from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Find Fruit',
            'Author': ['@424f424f'],
            'Description': ('Searches for low-hanging web applications.'),
            'Background' : True,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ['CIDR Parser credits to http://bibing.us.es/proyectos/abreproy/12106/fichero/ARCHIVOS%252Fservidor_xmlrpc%252Fcidr.py']
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Target' : {
                'Description'   :   'IP Address or CIDR to scan.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Port' : {
                'Description'   :   'The port to scan on.',
                'Required'      :   True,
                'Value'         :   '8080'
            },
            'SSL' : {
                'Description'   :   'True/False to force SSL',
                'Required'      :   False,
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
        target = self.options['Target']['Value']
        port = self.options['Port']['Value']
        ssl = self.options['SSL']['Value']
        script = """
import urllib2
import sys
import re
import subprocess
iplist = []
def ip2bin(ip):
    b = ""
    inQuads = ip.split(".")
    outQuads = 4
    for q in inQuads:
        if q != "":
            b += dec2bin(int(q),8)
            outQuads -= 1
    while outQuads > 0:
        b += "00000000"
        outQuads -= 1
    return b
def dec2bin(n,d=None):
    s = ""
    while n>0:
        if n&1:
            s = "1"+s
        else:
            s = "0"+s
        n >>= 1
    if d is not None:
        while len(s)<d:
            s = "0"+s
    if s == "": s = "0"
    return s
def bin2ip(b):
    ip = ""
    for i in range(0,len(b),8):
        ip += str(int(b[i:i+8],2))+"."
    return ip[:-1]
def printCIDR(c):
    parts = c.split("/")
    baseIP = ip2bin(parts[0])
    subnet = int(parts[1])
    if subnet == 32:
        print bin2ip(baseIP)
    else:
        ipPrefix = baseIP[:-(32-subnet)]
        for i in range(2**(32-subnet)):
            iplist.append(bin2ip(ipPrefix+dec2bin(i, (32-subnet))))
        return
def validateCIDRBlock(b):
    p = re.compile("^([0-9]{1,3}\.){0,3}[0-9]{1,3}(/[0-9]{1,2}){1}$")
    if not p.match(b):
        print "Error: Invalid CIDR format!"
        return False
    prefix, subnet = b.split("/")
    quads = prefix.split(".")
    for q in quads:
        if (int(q) < 0) or (int(q) > 255):
            print "Error: quad "+str(q)+" wrong size."
            return False
    if (int(subnet) < 1) or (int(subnet) > 32):
        print "Error: subnet "+str(subnet)+" wrong size."
        return False
    return True
def http_get(url):    
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req, timeout = 1)
    code = resp.getcode()
    if code == 200:
        print url + " returned 200!"
    return
def main(ip, port, ssl):
    if ssl == True:
        http = "https"
    elif ssl == False:
        http = "http"
    VulnLinks = []
    if '/' in ip:
        printCIDR(ip)
        for ip in iplist:
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "jmx-console/")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "web-console/ServerInfo.jsp")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "invoker/JMXInvokerServlet")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "lc/system/console")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "axis2/axis2-admin/")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "manager/html/")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "tomcat/manager/html/")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "wp-admin")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "workorder/FileDownload.jsp")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "ibm/console/logon.jsp?action=OK")
            VulnLinks.append(http + '://' + ip + ':' + port + '/' + "data/login")
    else:
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'jmx-console/')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'web-console/ServerInfo.jsp')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'invoker/JMXInvokerServlet')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'lc/system/console')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'axis2/axis2-admin/')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'manager/html/')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'tomcat/manager/html/')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'wp-admin')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'workorder/FileDownload.jsp')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'ibm/console/logon.jsp?action=OK')
        VulnLinks.append(http + '://' + ip + ':' + port + '/' + 'data/login')
    for link in VulnLinks:
        while True:
            try:
                req = urllib2.Request(link)
                resp = urllib2.urlopen(req, timeout = 1)
                code = resp.getcode()
                if code == 200:
                    print link + " returned 200!"
                break
            except urllib2.URLError:
                break  
ip = "%s"
port = str("%s")
ssl = %s
main(ip, port, ssl)
""" %(target, port, ssl)
        return script