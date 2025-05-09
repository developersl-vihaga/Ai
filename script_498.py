from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'User-to-SID',
            'Author': ['@harmj0y'],
            'Description': ("Converts a specified domain\\user to a domain sid."),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'powershell',
            'MinLanguageVersion' : '2',
            'Comments': []
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Domain' : {
                'Description'   :   'Domain name for translation.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'User' : {
                'Description'   :   'Username for translation.',
                'Required'      :   True,
                'Value'         :   ''
            }
        }
        self.mainMenu = mainMenu
        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = "(New-Object System.Security.Principal.NTAccount(\"%s\",\"%s\")).Translate([System.Security.Principal.SecurityIdentifier]).Value" %(self.options['Domain']['Value'], self.options['User']['Value'])
        if obfuscate:
            script = helpers.obfuscate(self.mainMenu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        return script