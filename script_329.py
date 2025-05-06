class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Change Login Message for the user.',
            'Author': ['@424f424f'],
            'Description': 'Change the login message for the user.',
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : True,
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
            'Message' : {
                'Description'   :   'Message to display',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Remove' : {
                'Description'   :   'True/False to remove login message.',
                'Required'      :   True,
                'Value'         :   'False'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        message = self.options['Message']['Value']
        remove = self.options['Remove']['Value']
        script = """
import subprocess
remove = %s
try:
    if remove == True:
        cmd = \"""defaults delete /Library/Preferences/com.apple.loginwindow LoginwindowText""\"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        print "Login message removed"
    elif remove == False:
        cmd = \"""defaults write /Library/Preferences/com.apple.loginwindow LoginwindowText '%s' ""\"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        print "Login message added"
    else:
        print "Invalid options"
except Exception as e:
    print "Module failed"
    print e
""" % (remove, message)
        return script