class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'dscl Get-Groups',
            'Author': ['@424f424f'],
            'Description': 'This module will use the current user context to query active directory for a list of Groups.',
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
            'Domain' : {
                'Description'   :   'Domain',
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
        script = """
import subprocess
cmd = \"""dscl "/Active Directory/%s/All Domains/" -list /Groups\"""
print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
""" % (domain)
        return script