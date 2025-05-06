import requests
print("""
<<<<<<<<<<<<<>>>>>>>>>>>>
      RXSS TESTER
<<<<<<<<<<<<<>>>>>>>>>>>>
""")
target = input("[ ? ] Set a site for rxss testing : ")
print("")
header = ""
payloads=open("payloads.txt","r")
for payload in payloads.readlines():
    target_with_payload = target+str(payload)
    testing = requests.get(url=target_with_payload, headers=header)
    if str(payload) in str(testing.text):
        print("[ + ] Possible XSS Found : ",str(payload))
    else:
        print("[ ! ] Nothing Found :( ")