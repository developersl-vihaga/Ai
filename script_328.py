class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Change Login Message for the user.',
            'Author': ['@424f424f'],
            'Description': 'Change the login message for the user.',
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
            'Image' : {
                'Description'   :   'Location of the image to use.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Desktop' : {
                'Description'   :   'True/False to change the desktop background.',
                'Required'      :   False,
                'Value'         :   'False'
            },
            'Login' : {
                'Description'   :   'True/False to change the login background.',
                'Required'      :   False,
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
        image = self.options['Image']['Value']
        desktop = self.options['Desktop']['Value']
        login = self.options['Login']['Value']
        script = """
import subprocess
desktop = %s
login = %s
if desktop == True:
    try:
        cmd = \"""osascript -e 'tell application "Finder" to set desktop picture to "%s" as POSIX file'""\"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        print "Desktop background changed!"
    except Exception as e:
        print "Changing desktop background failed"
        print e
if login == True:
    try:
        cmd = \"""cp %s /Library/Caches/com.apple.desktop.admin.png""\"
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        print "Login background changed!"
    except Exception as e:
        print "Changing login background failed"
        print e
""" % (desktop, login, image, image)
        return script