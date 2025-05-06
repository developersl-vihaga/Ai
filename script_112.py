import re
import sys
import os
import subprocess
import time
import signal
definepath = os.getcwd()
sys.path.append(definepath)
from src.core.setcore import *
operating_system = check_os()
me = mod_name()
def return_menu():
    print_status("Option added. You may select additional vectors")
    time.sleep(2)
    print("""\nSelect which additional attacks you want to use:\n""")
java_applet = "off"
meta_attack = "off"
harvester = "off"
tabnabbing = "off"
mlitm = "off"
webjacking = "off"
def flag_on(vector):
    print_info("Turning the %s Attack Vector to " %
               (vector) + bcolors.GREEN + "ON" + bcolors.ENDC)
def flag_off(vector):
    print_info("Turning the %s Attack Vector to " %
               (vector) + bcolors.RED + "OFF" + bcolors.ENDC)
def write_file(filename, results):
    filewrite = open(userconfigpath + "%s" % (filename), "w")
    filewrite.write(results)
    filewrite.close()
filewrite = open(userconfigpath + "attack_vector", "w")
filewrite.write("multiattack")
filewrite.close()
trigger = ""
toggleflag_java = (bcolors.RED + " (OFF)" + bcolors.ENDC)
toggleflag_meta = (bcolors.RED + " (OFF)" + bcolors.ENDC)
toggleflag_harv = (bcolors.RED + " (OFF)" + bcolors.ENDC)
toggleflag_tabnab = (bcolors.RED + " (OFF)" + bcolors.ENDC)
toggleflag_mlitm = (bcolors.RED + " (OFF)" + bcolors.ENDC)
toggleflag_webjacking = (bcolors.RED + " (OFF)" + bcolors.ENDC)
definepath = os.getcwd()
webdav_enable = "OFF"
clonedurl = 0
fileopen = open(userconfigpath + "site.template", "r")
data = fileopen.read()
if "TEMPLATE=SELF" in data:
    clonedurl = 1
if clonedurl == 0:
    subprocess.Popen("rm -rf %s/web_clone;mkdir %s/web_clone/" % (userconfigpath, userconfigpath),
                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
a = 1
print ("""
[*************************************************************]
                Multi-Attack Web Attack Vector
[*************************************************************]
 The multi attack vector utilizes each combination of attacks
 and allow the user to choose the method for the attack. Once
 you select one of the attacks, it will be added to your
 attack profile to be used to stage the attack vector. When
 your finished be sure to select the 'I'm finished' option.""")
print("""\nSelect which attacks you want to use:
""")
while a == 1:
    trigger = ""
    print("   1. Java Applet Attack Method" + toggleflag_java)
    print("   2. Metasploit Browser Exploit Method" + toggleflag_meta)
    print("   3. Credential Harvester Attack Method" + toggleflag_harv)
    print("   4. Tabnabbing Attack Method" + toggleflag_tabnab)
    print("   5. Web Jacking Attack Method" + toggleflag_webjacking)
    print("   6. Use them all - A.K.A. 'Tactical Nuke'")
    print("   7. I'm finished and want to proceed with the attack")
    print("\n  99. Return to Main Menu\n")
    profile = input(
        setprompt(["2", "16"], "Enter selections one at a time (7 to finish)"))
    if profile == "":
        profile = "7"
    try:    # this will trigger an error if it isnt an integer
        profile = int(profile)
        profile = str(profile)
    except:
        profile = "10"
    if profile == "99":
        break
    if int(profile) >= 10:
        input("\nInvalid option..")
        return_continue()
    if profile == "6":
        if operating_system == "windows":
            print_warning("Sorry this option is not available in Windows")
            return_continue()
        if operating_system != "windows":
            print(bcolors.RED + (r"""
                          ..-^~~~^-..
                        .~           ~.
                       (;:           :;)
                        (:           :)
                          ':._   _.:'
                              | |
                            (=====)
                              | |
                              | |
                              | |
                           ((/   \))""") + bcolors.ENDC)
            print("\nSelecting everything SET has in its aresenal, you like sending a nuke don't you?")
            print("\n[*] Note that tabnabbing is not enabled in the tactical nuke, select manually if you want.\n")
            java_applet = "on"
            meta_attack = "on"
            harvester = "on"
            break
    if profile == "7":
        break
    if profile == "1":
        if java_applet == "off":
            flag_on("Java Applet")
            return_menu()
            java_applet = "on"
            trigger = 1
            toggleflag_java = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
        if java_applet == "on":
            if trigger != 1:
                flag_off("Java Applet")
                return_menu()
                java_applet = "off"
                toggleflag_java = (bcolors.RED + " (OFF)" + bcolors.ENDC)
    if profile == "2":
        if operating_system == "windows":
            print_warning("Sorry this option is not available in Windows")
            return_continue()
        if operating_system != "windows":
            if meta_attack == "off":
                flag_on("Metasploit Client Side")
                return_menu()
                meta_attack = "on"
                trigger = 1
                toggleflag_meta = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
            if meta_attack == "on":
                if trigger != 1:
                    flag_off("Metasploit Client Side")
                    return_menu()
                    meta_attack = "off"
                    toggleflag_meta = (bcolors.RED + " (OFF)" + bcolors.ENDC)
    if profile == "3":
        if harvester == "off":
            flag_on("Harvester")
            return_menu()
            harvester = "on"
            trigger = 1
            toggleflag_harv = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
            if mlitm == "on":
                mlitm = "off"
                toggleflag_mlitm = (bcolors.RED + " (OFF)" + bcolors.ENDC)
        if harvester == "on":
            if trigger != 1:
                flag_off("Harvester")
                return_menu()
                harvester = "off"
                toggleflag_harv = (bcolors.RED + " (OFF)" + bcolors.ENDC)
    if profile == "4":
        if tabnabbing == "off":
            flag_on("Tabnabbing")
            return_menu()
            tabnabbing = "on"
            trigger = 1
            harvester = "on"
            toggleflag_tabnab = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
            if mlitm == "on":
                mlitm = "off"
                toggleflag_mlitm = (bcolors.RED + " (OFF)" + bcolors.ENDC)
            print(webjacking)
            if webjacking == "on":
                webjacking = "off"
                toggleflag_webjacking = (bcolors.RED + " (OFF)" + bcolors.ENDC)
        if tabnabbing == "on":
            if trigger != 1:
                flag_off("Tabnabbing")
                return_menu()
                tabnabbing = "off"
                harvester = "off"
                toggleflag_tabnab = (bcolors.RED + " (OFF)" + bcolors.ENDC)
    if profile == "5":
        if webjacking == "off":
            flag_on("Web Jacking")
            webjacking = "on"
            return_menu()
            trigger = 1
            if tabnabbing == "on" or mlitm == "on":
                print("[*] You cannot use MLITM and Tabnabbing in the same attack!")
                print("[*] Disabling MLITM and/or Tabnabbing")
                mlitm = "off"
                tabnabbing = "off"
                harvester = "on"
                toggleflag_mlitm = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
                toggleflag_tabnab = (bcolors.RED + " (OFF)" + bcolors.ENDC)
                toggleflag_harv = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
            if harvester == "off":
                harvester = "on"
                toggleflag_harv = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
            toggleflag_webjacking = (bcolors.GREEN + " (ON)" + bcolors.ENDC)
        if webjacking == "on":
            if trigger != 1:
                flag_off("Web Jacking")
                return_menu()
                webjacking = "off"
                toggleflag_webjacking = (bcolors.RED + " (OFF)" + bcolors.ENDC)
payloadgen = 0
if java_applet == "on":
    write_file("multi_java", "multiattack=java_on")
if meta_attack == "on":
    write_file("multi_meta", "multiattack=meta_on")
if tabnabbing == "on":
    write_file("multi_tabnabbing", "multiattack=tabnabbing_on")
if harvester == "on":
    write_file("multi_harvester", "multiattack=harvester_on")
if mlitm == "on":
    write_file("multi_mlitm", "multiattack=mlitm_on")
if webjacking == "on":
    write_file("multi_webjacking", "multiattack=webjacking_on")
if java_applet == "on" or meta_attack == "on" or harvester == "on" or tabnabbing == "on" or mlitm == "on":
    sys.path.append("src/webattack/web_clone")
    debug_msg(me, "importing 'src.webattack.web_clone.cloner'", 1)
    try:
        module_reload(cloner)
    except:
        import cloner
    if operating_system != "windows":
        sys.path.append("src/core/arp_cache")
        debug_msg(me, "importing 'src.core.arp_cache.arp'", 1)
        try:
            module_reload(arp)
        except:
            import arp
if java_applet == "on":
    sys.path.append("src/core/payloadgen/")
    debug_msg(me, "importing 'src.core.payloadgen.create_payloads'", 1)
    try:
        module_reload(create_payloads)
    except:
        import create_payloads
    payloadgen = 1
    applet_choice()
if meta_attack == "on":
    sys.path.append("src/webattack/browser_exploits/")
    import gen_payload
    if os.path.isfile(userconfigpath + "webdav_enabled"):
        webdav_enabled = "on"
pexpect_flag = "off"
if harvester == "on" or tabnabbing == "on" or webjacking == "on":
    if tabnabbing == "on" or webjacking == "on":
        sys.path.append("src/webattack/tabnabbing")
        debug_msg(me, "importing 'src.webattack.tabnabbing.tabnabbing'", 1)
        try:
            module_reload(tabnabbing)
        except:
            import tabnabbing
    sys.path.append("src/webattack/harvester")
    if java_applet == "on" or meta_attack == "on":
        pexpect_flag = "on"
        a = subprocess.Popen(
            "python src/webattack/harvester/harvester.py", shell=True)
if mlitm == "on":
    sys.path.append("src/webattack/mlitm")
    if java_applet == "on" or meta_attack == "on":
        a = subprocess.Popen("python src/mlitm/mlitm.py")
    else:
        debug_msg(me, "importing 'src.mlitm.mlitm'", 1)
        try:
            module_reload(mlitm)
        except:
            import mlitm
if java_applet == "on" or meta_attack == "on":
    sys.path.append("src/html/")
    debug_msg(me, "importing 'src.html.spawn'", 1)
    try:
        module_reload(spawn)
    except:
        import spawn
    if harvester == "on" or tabnabbing == "on":
        os.chdir(definepath)
        sys.path.append("%s/src/webattack/harvester/" % (definepath))
        import report_generator
        try:
            a.terminate()
        except AttributeError:
            os.kill(a.pid, signal.SIGTERM)
        print_status("\nReport exported.")
        return_continue()