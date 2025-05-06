class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Background Example',
            'Author': ['@Killswitch-GUI'],
            'Description': ('A quick example how to feed your data to a background job.'),
            'Background' : True,
            'OutputExtension' : '',
            'NeedsAdmin' : False,
            'OpsecSafe' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [ ]
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
    def generate(self):
        script = """
x = 0
while True:
    import time
    try:
        time.sleep(2)
        msg = 'NOW inside buffer at message: ' + str(x) + '\\n'
        job_message_buffer(msg)
        x += 1
    except Exception as e:
        print e
"""
        return script