class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Get Domain Controllers',
            'Author': ['@424f424f'],
            'Description': 'This module will list all domain controllers from active directory',
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
                'Description'   :   'Agent to run on.',
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
cmd = \"""ldapsearch -x -h {} -b "dc={},dc={}" -D {} -w {} "(&(objectcategory=Computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))" ""\".format(LDAPAddress, tld, ext, BindDN, password)
output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
output2 = subprocess.Popen(["grep", "name:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
output.stdout.close()
out,err = output2.communicate()
print ""
print out
""" % (BindDN, LDAPAddress, password)
        return script