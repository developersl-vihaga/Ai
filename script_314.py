from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'SSHCommand',
            'Author': ['@424f424f'],
            'Description': 'This module will send a command via ssh.',
            'Background' : True,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                'http://stackoverflow.com/questions/17118239/how-to-give-subprocess-a-password-and-get-stdout-at-the-same-time'
                            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to use ssh from.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Login' : {
                'Description'   :   'user@127.0.0.1',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Password' : {
                'Description'   :   'Password',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Command' : {
                'Description'   :   'Command',
                'Required'      :   True,
                'Value'         :   'id'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        login = self.options['Login']['Value']
        password = self.options['Password']['Value']
        command = self.options['Command']['Value']
        script = """
import os
import pty
def wall(host, pw):
    import os,pty
    pid, fd = pty.fork()
    if pid == 0: # Child
        os.execvp('ssh', ['ssh', '-o StrictHostKeyChecking=no', host, '%s'])
        os._exit(1) # fail to execv
    os.read(fd, 1024)
    os.write(fd, '\\n' + pw + '\\n')
    result = []
    while True:
        try:
            data = os.read(fd, 1024)
            if data[:8] == "Password" and data[-1:] == ":":
                os.write(fd, pw + '\\n')
        except OSError:
            break
        if not data:
            break
        result.append(data)
    pid, status = os.waitpid(pid, 0)
    return status, ''.join(result)
status, output = wall('%s','%s')
print status
print output
""" % (command, login, password)
        return script