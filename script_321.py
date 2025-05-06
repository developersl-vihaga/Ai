from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'RemoveLaunchDaemon',
            'Author': ['@xorrior'],
            'Description': ('Remove an Empire Launch Daemon.'),
            'Background' : False,
            'OutputExtension' : None,
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
            },
            'PlistPath' : {
                'Description'   :   'Full path to the plist file to remove.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'ProgramPath' : {
                'Description'   :   'Full path to the bash script/ binary file to remove.',
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
        plistpath = self.options['PlistPath']['Value']
        programpath = self.options['ProgramPath']['Value']
        script = """
import subprocess 
process = subprocess.Popen('launchctl unload %s', stdout=subprocess.PIPE, shell=True)
process.communicate()
process = subprocess.Popen('rm %s', stdout=subprocess.PIPE, shell=True)
process.communicate()
process = subprocess.Popen('rm %s', stdout=subprocess.PIPE, shell=True)
process.communicate()
print "\\n [+] %s has been removed"
print "\\n [+] %s has been removed"
""" %(plistpath,plistpath,programpath,plistpath,programpath)
        return script