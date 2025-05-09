"""
HTTP related methods used by Empire.
Includes URI validation/checksums, as well as the base
http server (EmpireServer) and its modified request
handler (RequestHandler).
These are the first places URI requests are processed.
"""
from BaseHTTPServer import BaseHTTPRequestHandler
import BaseHTTPServer, threading, ssl, os, string, random
from pydispatch import dispatcher
import re
import json
import encryption
import helpers
def default_page():
    """
    Returns the default page for this server.
    """
    page = "<html><body><h1>It works!</h1>"
    page += "<p>This is the default web page for this server.</p>"
    page += "<p>The web server software is running but no content has been added, yet.</p>"
    page += "</body></html>"
    return page
def host2lhost(s):
    """
    Return lhost for Empire's native listener from Host value
    """
    reg = r'(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
    res = re.findall( reg, s)
    return res[0] if len(res) == 1 else '0.0.0.0'
def checksum8(s):
    """
    Add up all character values and mods the total by 256.
    """
    return sum([ord(ch) for ch in s]) % 0x100
class RequestHandler(BaseHTTPRequestHandler):
    """
    Main HTTP handler we're overwriting in order to modify the HTTPServer behavior.
    """
    serverVersion = helpers.get_config('server_version')[0]
    BaseHTTPRequestHandler.server_version = serverVersion
    BaseHTTPRequestHandler.sys_version = ""
    def do_GET(self):
        resource = self.path
        clientIP = self.client_address[0]
        sessionID = None
        cookie = self.headers.getheader("Cookie")
        if cookie:
            parts = cookie.split(";")
            for part in parts:
                if "SESSIONID" in part:
                    name, sessionID = part.split("=", 1)
        message = "[*] {resource} requested from {session_id} at {client_ip}".format(
            resource=resource,
            session_id=sessionID,
            client_ip=clientIP
        )
        signal = json.dumps({
            'print': True,
            'message': message
        })
        dispatcher.send(signal, sender="empire")
        (code, responsedata) = self.server.agents.process_get(self.server.server_port, clientIP, sessionID, resource)
        self.send_response(code)
        self.end_headers()
        self.wfile.write(responsedata)
        self.wfile.flush()
    def do_POST(self):
        resource = self.path
        clientIP = self.client_address[0]
        sessionID = None
        cookie = self.headers.getheader("Cookie")
        if cookie:
            parts = cookie.split(";")
            for part in parts:
                if "SESSIONID" in part:
                    name, sessionID = part.split("=", 1)
        message = "[*] Post to {resource} from {session_id} at {client_ip}".format(
            resource=resource,
            session_id=sessionID,
            client_ip=clientIP
        )
        signal = json.dumps({
            'print': True,
            'message': message
        })
        dispatcher.send(signal, sender="empire")
        if self.headers.getheader('content-length'):
            length = int(self.headers.getheader('content-length'))
            postData = self.rfile.read(length)
            (code, responsedata) = self.server.agents.process_post(self.server.server_port, clientIP, sessionID, resource, postData)
            self.send_response(code)
            self.end_headers()
            self.wfile.write(responsedata)
            self.wfile.flush()
    def log_message(*arg):
        pass
class EmpireServer(threading.Thread):
    """
    Version of a simple HTTP[S] Server with specifiable port and
    SSL cert. Defaults to HTTP is no cert is specified.
    Uses agents.RequestHandler handle inbound requests.
    """
    def __init__(self, handler, lhost='0.0.0.0', port=80, cert=''):
        self.success = True
        try:
            threading.Thread.__init__(self)
            self.server = None
            self.server = BaseHTTPServer.HTTPServer((lhost, int(port)), RequestHandler)
            self.server.agents = handler
            self.port = port
            self.serverType = "HTTP"
            if cert and cert != "":
                self.serverType = "HTTPS"
                cert = os.path.abspath(cert)
                self.server.socket = ssl.wrap_socket(self.server.socket, certfile=cert, server_side=True)
                message = "[*] Initializing HTTPS server on {port}".format(port=port)
            else:
                message = "[*] Initializing HTTP server on {port}".format(port=port)
            signal = json.dumps({
                'print': True,
                'message': message
            })
            dispatcher.send(signal, sender="empire")
        except Exception as e:
            self.success = False
            message = "[!] Error starting listener on port {}: {}".format(port, e)
            signal = json.dumps({
                'print': True,
                'message': message
            })
            dispatcher.send(signal, sender="empire")
    def base_server(self):
        return self.server
    def run(self):
        try: self.server.serve_forever()
        except: pass
    def shutdown(self):
        self.server.shutdown()
        self.server.socket.close()
        self.server.server_close()
        self._Thread__stop()
        for thread in threading.enumerate():
            if thread.isAlive():
                try:
                    thread._Thread__stop()
                except:
                    pass