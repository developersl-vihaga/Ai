import subprocess
import os
try:
    print("""
Simply enter in the required fields, easy example below:
Name: FakeCompany
Organization: Fake Company
Organization Name: Fake Company
City: Cleveland
State: Ohio
Country: US
Is this correct: yes
""")
    print("""*** WARNING ***\nIN ORDER FOR THIS TO WORK YOU MUST INSTALL sun-java6-jdk or openjdk-6-jdk, so apt-get install openjdk-6-jdk\n*** WARNING ***""")
    subprocess.Popen(
        "keytool -genkey -alias signapplet2 -keystore mykeystore -keypass mykeypass -storepass mystorepass", shell=True).wait()
    subprocess.Popen(
        "jarsigner -keystore mykeystore -storepass mystorepass -keypass mykeypass -signedjar Signed_Update.jar Java_Obf.jar signapplet2", shell=True).wait()
    subprocess.Popen("rm ../../html/Signed_Update.jar.orig", shell=True).wait()
    subprocess.Popen(
        "cp Signed_Update.jar ../../html/Signed_Update.jar.orig", shell=True).wait()
    subprocess.Popen(
        "cp Java_Obf.jar ../../html/unsigned/unsigned.jar", shell=True).wait()
    print("[*] New java applet has been successfully imported into The Social-Engineer Toolkit (SET)")
except:
    pass