class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Get Users',
            'Author': ['@424f424f'],
            'Description': 'This module list users found in Active Directory',
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ['']
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to grab run on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'LDAPAddress' : {
                'Description'   :   'LDAP IP/Hostname',
                'Required'      :   True,
                'Value'         :   ''
            },
            'BindDN' : {
                'Description'   :   'user@penlab.local',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Password' : {
                'Description'   :   'Password to connect to LDAP',
                'Required'      :   False,
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
        LDAPAddress = self.options['LDAPAddress']['Value']
        BindDN = self.options['BindDN']['Value']
        password = self.options['Password']['Value']
        script = """
import sys, os, subprocess, re
BindDN = "%s"
LDAPAddress = "%s"
password = "%s"
regex = re.compile('.+@([^.]+)\..+')
global tld
match = re.match(regex, BindDN)
tld = match.group(1)
global ext
ext = BindDN.split('.')[1]
cmd = \"""ldapsearch -x -h {} -b "dc={},dc={}" -D {} -w {} "objectclass=user" sAMAccountName""\".format(LDAPAddress, tld, ext, BindDN, password)
output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, bufsize=1)
with output.stdout:
    print ""
    for line in iter(output.stdout.readline, b''):
        if ("sAMAccountName:") in line:
            if '$' not in line:
                m = re.search(r'[^sAMAccountName:].*$', line)
                print m.group(0).lstrip()
output.wait()
print ""
""" % (BindDN, LDAPAddress, password)
        return script