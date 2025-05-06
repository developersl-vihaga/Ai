class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Say',
            'Author': ['@harmj0y'],
            'Description': ('Performs text to speech using "say".'),
            'Background' : False,
            'OutputExtension' : '',
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [ ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Text' : {
                'Description'   :   'The text to speak.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Voice' : {
                'Description'   :   'The voice to use.',
                'Required'      :   True,
                'Value'         :   'alex'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        voice = self.options['Voice']['Value']
        text = self.options['Text']['Value']
        script = """
run_command('say -v %s %s')
""" % (voice, text)
        return script