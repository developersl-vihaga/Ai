from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Translate a host name to IPv4 address format using a remote agent.',
            'Author': ['@TweekFawkes'],
            'Description': ('Uses Python\'s socket.gethostbyname("example.com") function to resolve host names on a remote agent.'),
            'Background' : True,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ['none']
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Target' : {
                'Description'   :   'FQDN, domain name, or hostname to lookup using the remote target.',
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
        target = self.options['Target']['Value']
        script = """
import socket
def main(target):
    return_Str = ''
    try:
        return_Str = str(socket.gethostbyname(target))
        print "{} resolved to {} !".format(target, return_Str)
    except socket.error:
        print "{} failed to resolve :(".format(target)
target = "%s"
main(target)
""" %(target)
        return script