from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Search for world writeable files',
            'Author': ['@424f424f'],
            'Description': ('This module can be used to identify world writeable files.'),
            'Background' : True,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                ''
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run the module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Path' : {
                'Description'   :   'Path to start the search from. Default is / ',
                'Required'      :   True,
                'Value'         :   '/'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
       	path = self.options['Path']['Value']
        script = """
import os
import subprocess
cmd = "find %s -xdev -type d \( -perm -0002 -a ! -perm -1000 \) -print"
print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
""" % (path)
        return script