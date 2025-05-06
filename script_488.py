from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'SID-to-User',
            'Author': ['@harmj0y'],
            'Description': ("Converts a specified domain sid to a user."),
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
            'SID' : {
                'Description'   :   'Domain SID to translate.',
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
        script = "(New-Object System.Security.Principal.SecurityIdentifier(\"%s\")).Translate( [System.Security.Principal.NTAccount]).Value" %(self.options['SID']['Value'])
        if obfuscate:
            script = helpers.obfuscate(self.mainMenu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        return script