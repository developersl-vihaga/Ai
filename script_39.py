from main.tools import run_on_browser,colors,banner,template
import os
import threading
def writeup(writeup_dist,name):
    while True:
        os.system("clear")
        banner.main()
        banner.attack(name.title())
        key=list(writeup_dist.keys())
        key.append("Go Back")
        for i in range(len(key)):
            print(colors.options,f"{i+1}) {key[i]}".title(),colors.reset)
        try:
            option =input(f"\n {colors.select}Select An Option -> {colors.reset} ")
        except KeyboardInterrupt:
            return
        try:
            threading.Thread(target=run_on_browser.main, args=(writeup_dist[key[(int(option))-1]],)).start()
        except:
            return