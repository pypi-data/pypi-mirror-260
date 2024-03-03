#!/usr/bin/env python3
import http.server
import http.client
import http.cookies
import random
import time
import threading
import struct
import errno
import socket
import ssl
import json
import re
import argparse
from base64 import b64encode
from socketserver import ThreadingMixIn
from hashlib import sha1
import websocket

parser = argparse.ArgumentParser(description='Smart loadbalancer for Odoo')
parser.add_argument('-c','--config', help='configuration file (json format)', required=True)
args = vars(parser.parse_args())

CONFIG ={}
with open(args['config'], "r") as f :
    CONFIG = json.load(f)

def is_static_path(path):
    for rule in  CONFIG.get('read_rules', []) :
        if re.match(rule, path) : return True
    return False

def select_srv(type, session=False):
    global CONFIG

    if CONFIG['distribution'] == 'random'  or ( CONFIG['distribution'] == 'session' and not session ):
        return CONFIG[type][random.randint(0, len(CONFIG[type])-1)]
    
    if CONFIG['distribution'] == 'robin' :
        key = type + '_' + CONFIG['distribution']
        next = CONFIG.get(key, 0)
        next = (next + 1) if (next + 1) < len(CONFIG[type]) else 0
        CONFIG[key] = next
        return CONFIG[type][CONFIG[key]]

    if CONFIG['distribution'] == 'session' :
        affected = 10000
        cible  = 0
        for index, value in enumerate(CONFIG[type]) :
            if not CONFIG['distribution'] in CONFIG[type][index].keys() : CONFIG[type][index][CONFIG['distribution']] = []
            if session in CONFIG[type][index][CONFIG['distribution']] :
                return CONFIG[type][index]
            
            if len(CONFIG[type][index][CONFIG['distribution']]) <= affected :
                cible = index
                affected = len(CONFIG[type][index][CONFIG['distribution']])
        
        CONFIG[type][cible][CONFIG['distribution']].append(session)
        return CONFIG[type][cible]


    if CONFIG['distribution'] == 'availability' :
        active = 10000
        cible  = 0
        for index, value in enumerate(CONFIG[type]) :
            if not CONFIG['distribution'] in CONFIG[type][index].keys() : CONFIG[type][index][CONFIG['distribution']] = 0
            if CONFIG[type][index][CONFIG['distribution']] <= active :
                cible = index
                active = CONFIG[type][index][CONFIG['distribution']]
        
        CONFIG[type][cible][CONFIG['distribution']] += 1
        return CONFIG[type][cible]

class WebSocketError(Exception):
    pass

class ThreadingHTTPServer(ThreadingMixIn, http.server.HTTPServer):
    pass

class ProxyHandler(http.server.BaseHTTPRequestHandler):
    _ws_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    _opcode_continu = 0x0
    _opcode_text = 0x1
    _opcode_binary = 0x2
    _opcode_close = 0x8
    _opcode_ping = 0x9
    _opcode_pong = 0xa

    ws = None
    daemon_threads = True
    mutex = threading.Lock()

##############################################
#
#               COMMON
#
##############################################                        
    def log_message(self, format, *args):
        super().log_message(format, *args)

    def setup(self):
        super().setup()
        self.connected = False

##############################################
#
#               WS
#
##############################################                        

    def on_ws_message(self, message):
        if self.ws : self.ws.send(message)
        pass
        
    def on_ws_connected(self):
        def on_message(clt, message):
            if isinstance(message, str) :
                message = message.encode('utf-8')
            self.send_message(message)

        def on_close(ws):
            pass
        def on_open(ws):
            pass
        
        self.ws = websocket.WebSocketApp("ws://%s:%s/websocket" %(CONFIG['ws_srv']["host"], CONFIG['ws_srv']["port"]), cookie = self.headers.get('Cookie', None), on_message = on_message, on_close = on_close, on_open = on_open)
        tmp = threading.Thread(target=self.ws.run_forever)
        tmp.daemon = True
        tmp.start()
        pass
        
    def on_ws_closed(self):
        """Override this handler."""
        if self.ws : self.ws.close()

        pass
        
    def send_message(self, message):
        self._send_message(self._opcode_text, message)

    def _read_messages(self):
        while self.connected == True:
            try:
                self._read_next_message()
            except (socket.error, WebSocketError) as e:
                #websocket content error, time-out or disconnect.
                self.log_message("RCV: Close connection: Socket Error %s" % str(e.args))
                self._ws_close()
            except Exception as err:
                #unexpected error in websocket connection.
                self.log_error("RCV: Exception: in _read_messages: %s" % str(err.args))
                self._ws_close()
        
    def _read_next_message(self):
        try:
            self.opcode = ord(self.rfile.read(1)) & 0x0F
            length = ord(self.rfile.read(1)) & 0x7F
            if length == 126:
                length = struct.unpack(">H", self.rfile.read(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self.rfile.read(8))[0]

            masks = [b for b in self.rfile.read(4)]
            decoded = ""
            for char in self.rfile.read(length):
                decoded += chr(char ^ masks[len(decoded) % 4])
            self._on_message(decoded)

        except (struct.error, TypeError) as e:
            #catch exceptions from ord() and struct.unpack()
            if self.connected:
                raise WebSocketError("Websocket read aborted while listening %s " %e) 
            else:
                #the socket was closed while waiting for input
                self.log_error("RCV: _read_next_message aborted after closed connection")
                pass
        
    def _send_message(self, opcode, message):
        try:
            header  = bytearray()
            header.append(0x80 | opcode)
            length = len(message)

            # Petit message
            if length <= 125:
                header.append(length)

            # Message < 16bits
            elif length >= 126 and length <= 65535:
                header.append(0x7e)
                header.extend(struct.pack(">H", length))
            
            # Message < 64bits
            elif length < 18446744073709551616:
                header.append(0x7f)
                header.extend(struct.pack(">Q", length))

            if length > 0:
                self.request.send(header + message)

        except socket.error as e:
            #websocket content error, time-out or disconnect.
            self.log_message("SND: Close connection: Socket Error %s" % str(e.args))
            self._ws_close()
        except Exception as err:
            #unexpected error in websocket connection.
            self.log_error("SND: Exception: in _send_message: %s" % str(err.args))
            self._ws_close()

    def _handshake(self):
        headers=self.headers
        if headers.get("Upgrade", None) != "websocket":
            return
        key = headers['Sec-WebSocket-Key']
        digest = b64encode(bytes.fromhex(sha1((key + self._ws_GUID).encode('utf-8')).hexdigest())).decode('utf-8')
        self.send_response(101, 'Switching Protocols')
        self.send_header('Upgrade', 'websocket')
        self.send_header('Connection', 'Upgrade')
        self.send_header('Sec-WebSocket-Accept', str(digest))
        self.end_headers()
        self.connected = True
        self.on_ws_connected()
    
    def _ws_close(self):
        #avoid closing a single socket two time for send and receive.
        self.mutex.acquire()
        try:
            if self.connected:
                self.connected = False
                self.close_connection = 1
                try: 
                    self._send_close()
                except:
                    pass
                self.on_ws_closed()
            else:
                self.log_message("_ws_close websocket in closed state. Ignore.")
                pass
        finally:
            self.mutex.release()
            
    def _on_message(self, message):
        if self.opcode == self._opcode_close:
            self.connected = False
            self.close_connection = 1
            try:
                self._send_close()
            except:
                pass
            self.on_ws_closed()
        # ping
        elif self.opcode == self._opcode_ping:
            self._send_message(self._opcode_pong, message)
        # pong
        elif self.opcode == self._opcode_pong:
            pass
        # data
        elif (self.opcode == self._opcode_continu or 
                self.opcode == self._opcode_text or 
                self.opcode == self._opcode_binary):
            self.on_ws_message(message)

    def _send_close(self):
        msg = bytearray()
        msg.append(0x80 + self._opcode_close)
        msg.append(0x00)
        self.request.send(msg)

##############################################
#
#               HTTP
#
##############################################                        
    def do_GET(self):
        if self.headers.get("Upgrade", None) == "websocket":
            self._handshake()
            self._read_messages()
        elif self.path == "/fortitude-reload" :
            with open("config.json", "r") as f :
                global CONFIG
                CONFIG = json.load(f)
        elif self.path == "/fortitude-status" :
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps(CONFIG, indent=4).encode())
        else:
            self.handle_request('GET')

    def do_POST(self):
        self.handle_request('POST')

    def do_PUT(self):
        self.handle_request('PUT')

    def do_DELETE(self):
        self.handle_request('DELETE')

    def do_HEAD(self):
        self.handle_request('HEAD')

    def handle_request(self, method):
        srv = False
        session = False
        if CONFIG['distribution'] == 'session' and self.headers.get('Cookie') :
            tmp = http.cookies.SimpleCookie()
            tmp.load(self.headers['Cookie'])
            session = tmp['session_id'].value if tmp.get('session_id', False) else False

        if is_static_path(self.path) :
            srv = select_srv('read_srv', session)
            conn = http.client.HTTPConnection(srv["host"], srv["port"])
            post_body=""
            content_len = int(self.headers.get('Content-Length', "0"))
            if content_len :
                post_body = self.rfile.read(content_len)
            conn.request(method, self.path, post_body, headers=self.headers)
        
        else :
            #Todo method
            srv = select_srv('write_srv', session)
            conn = http.client.HTTPConnection(srv["host"], srv["port"])

            post_body=""
            content_len = int(self.headers.get('Content-Length', "0"))
            if content_len :
                post_body = self.rfile.read(content_len)
            conn.request(method, self.path, post_body, headers=self.headers)

        response = conn.getresponse()
        self.send_response(response.status)
        for header, value in response.getheaders():
            self.send_header(header, value)
        self.end_headers()

        self.wfile.write(response.read())
        conn.close()

        if CONFIG['distribution'] == 'availability' :
            srv[CONFIG['distribution']] -= 1





if __name__ == '__main__':
    server_address = (CONFIG.get('http_bind', '0.0.0.0'), CONFIG.get('http_port', 80))
    httpd = ThreadingHTTPServer(server_address , ProxyHandler)

    if CONFIG.get("secure", False) :
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(CONFIG['secure_cert'], CONFIG['secure_key'])
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
    
    print('Reverse proxy server running on port %s...' %CONFIG.get('http_port', 80))
    httpd.serve_forever()
