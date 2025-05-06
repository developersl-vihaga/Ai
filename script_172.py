import glob
import re
import sys
from src.core.setcore import *
menu_return = "false"
counter = 0
print("\n")
print_info_spaces("Social-Engineer Toolkit Third Party Modules menu.")
print_info_spaces(
    "Please read the readme/modules.txt for information on how to create your own modules.\n")
for name in glob.glob("modules/*.py"):
    counter = counter + 1
    fileopen = open(name, "r")
    for line in fileopen:
        line = line.rstrip()
        match = re.search("MAIN=", line)
        if match:
            line = line.replace('MAIN="', "")
            line = line.replace('"', "")
            line = "  " + str(counter) + ". " + line
            print(line)
print("\n  99. Return to the previous menu\n")
choice = raw_input(setprompt(["9"], ""))
if choice == 'exit':
    exit_set()
if choice == '99':
    menu_return = "true"
try:
    choice = int(choice)
except:
    print_warning("An integer was not used try again")
    choice = raw_input(setprompt(["9"], ""))
counter = 0
if menu_return == "false":
    for name in glob.glob("modules/*.py"):
        counter = counter + 1
        if counter == int(choice):
            name = name.replace("modules/", "")
            name = name.replace(".py", "")
            sys.path.append("modules/")
            try:
                exec("import " + name)
            except:
                pass
            try:
                exec("%s.main()" % (name))
            except Exception as e:
                raw_input("   [!] There was an issue with a module: %s." % (e))
                return_continue()