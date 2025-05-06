from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'HTTP REST API',
            'Author': ['@TweekFawkes',"@scottjpack"],
            'Description': ('Interacts with a HTTP REST API and returns the results back to the screen.'),
            'Background' : True,
            'OutputExtension': "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ["Docs: https://mesos.github.io/chronos/docs/api.html", "urllib2 DELETE method credits to: http://stackoverflow.com/questions/21243834/doing-put-using-python-urllib2"]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Protocol' : {
                'Description'   :   'Protocol or Scheme to use.',
                'Required'      :   True,
                'Value'         :   'http'
            },
            'Target' : {
                'Description'   :   'FQDN, domain name, or hostname of the remote target.',
                'Required'      :   True,
                'Value'         :   'master.mesos'
            },
            'Port' : {
                'Description'   :   'The port to connect to.',
                'Required'      :   True,
                'Value'         :   '8123'
            },
            'Path' : {
                'Description'   :   'The path.',
                'Required'      :   True,
                'Value'         :   '/v1/version'
            },
            'RequMethod' : {
                'Description'   :   'The HTTP request method to use.',
                'Required'      :   True,
                'Value'         :   'GET'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        protocol = self.options['Protocol']['Value']
        target = self.options['Target']['Value']
        port = self.options['Port']['Value']
        path = self.options['Path']['Value']
        requmethod = self.options['RequMethod']['Value']
        script = """
import urllib2
protocol = "%s"
target = "%s"
port = "%s"
path = "%s"
requmethod = "%s"
url = protocol + "://" + target + ":" + port + path
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
    request = MethodRequest(url, method=requmethod)
    request.add_header('User-Agent',
                   'Mozilla/6.0 (X11; Linux x86_64; rv:24.0) '
                   'Gecko/20140205     Firefox/27.0 Iceweasel/25.3.0')
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    content = opener.open(request).read()
    print str(content)
except Exception as e:
    print "Failure sending payload: " + str(e)
print "Finished"
""" %(protocol, target, port, path, requmethod)
        return script