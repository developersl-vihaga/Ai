from main.tools import banner, colors, template,Exploitation_Tools
import os
import requests
from bs4 import BeautifulSoup
def main():
    while True:
        os.system("clear")
        banner.main()
        banner.attack("Post Exploitation")
        list_attacks = [" Metasploit-Framework\t\t(Recommended)", " LinPeas", " LinEnum", " Sudo killer\t\t\t(Recommended)", " Beroot", " Linux Exploit Suggester 2", " LSE (Linux Smart Enumeration) ",
                        " PSPY","Linux Private-i", "Shellter", "UPX (Ultimate Packer for Executable)", "Go Back"]
        for i in range(len(list_attacks)):
            print(colors.options, f"{i+1}) {list_attacks[i]}".title(), colors.reset)
        try:
            option = input(
                f"\n {colors.select}Select An Option ->{colors.reset}  ")
        except KeyboardInterrupt:
            return
        if option == "1":
            print("\n[+] Metasploit-Framework")
            Exploitation_Tools.metasploit()    
        elif option == "2":
            print("\n[+] LinPeas")
            linpeas()        
        elif option == "3":
            print("\n[+] LinEnum")
            linenum()       
        elif option == "4":
            print("\n[+] Sudo killer")
            sudokiller()    
        elif option == "5":
            print("\n[+] Beroot")
            beroot()        
        elif option == "6":
            print("\n[+] Linux Exploit Suggester 2")
            linux_exploit_suggester2()        
        elif option == "7":
            print("\n[+] LSE (Linux Smart Enumeration)")
            linux_smart_enumeration()        
        elif option == "8":
            print("\n[+] PSPY")
            pspy()       
        elif option == "9":
            print("\n[+] Linux Private-i")
            linux_private_i()        
        elif option == "10":
            print("\n[+] Shellter")
            shelter()        
        elif option == "11":
            print("\n[+] UPX (Ultimate Packer for Executable)")
            upx()        
        else:
            return
def github_getting_text(link, selector, indexvalue):
    print("Please Wait....\r", end="")
    URL = link
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        paras = soup.select(selector)
        return paras[indexvalue].text
    except:
         return f"{colors.red}Not Loaded Because No Internet Connection{colors.reset}"
def upx():
    os.system("clear")
    github = "UPX is a free, portable, extendable, high-performance executable packer for several different executable formats. It can be used to compress and obfuscate executable files to make them smaller and more difficult to reverse engineer. UPX supports a wide range of file formats, including Windows PE, Linux ELF, and more. UPX is available for a variety of platforms, including Windows, Linux, and macOS. The UPX compression algorithm is designed to compress the code section of an executable file, while leaving the data section uncompressed. This allows the compressed code to be executed directly from memory without the need to decompress it first. UPX is open-source and actively maintained, with updates and bug fixes released regularly."
    template.template("UPX (Ultimate Packer for Executable)", "chmod u+x upx && ./upx", github.strip(), {"UPX README": "https://github.com/upx/upx#readme", "UPX Video - 1 ": "https://www.youtube.com/watch?v=upTXpDhI0ww"}, method="github",
                              github_install="wget  https://github.com/upx/upx/releases/download/v4.0.1/upx-4.0.1-i386_linux.tar.xz  && tar -xf upx-4.0.1-i386_linux.tar.xz && rm upx-4.0.1-i386_linux.tar.xz", github_check="upx-4.0.1-i386_linux")
def shelter():
    os.system("clear")
    github = "Shellter is a dynamic shellcode injection tool aka dynamic PE infector. It can be used in order to inject shellcode into native Windows applications (currently 32-bit apps only). The shellcode can be something yours or something generated through a framework, such as Metasploit. Shellter takes advantage of the original structure of the PE file and doesn't apply any  modification such as changing memory access permissions in sections (unless the user wants to), adding an extra section with RWE access, and whatever would look dodgy under an AV scan. Shellter is not just an EPO infector that tries to find a location to insert an instruction to redirect execution to the payload. Unlike any other infector, Shellter’s advanced infection engine never transfers the execution flow to a code cave or to an added section in the infected PE file. Shellter uses a unique dynamic approach which is based on the execution flow of the target application. This means that no static/predefined locations are used for shellcode injection. Shellter will launch and trace the target, while at the same time will log the execution flow of the application."
    template.template("shellter", "shellter", github.strip(), {"Introduction to Shellter": "https://github.com/ParrotSec/shellter#readme", "Tool documentation for Shellter on Kali Linux": "https://www.kali.org/tools/shellter/#tool-documentation", "Anti-virus Bypass with Shellter 5.1 on Kali Linux": "https://cyberarms.wordpress.com/2015/10/04/anti-virus-bypass-with-shellter-5-1-on-kali-linux/",
                              "Shellter: A Shellcode Injecting Tool": "https://www.hackingarticles.in/shellter-a-shellcode-injecting-tool/", "Shellter - The Ultimate Tool for AV Evasion": "https://metalkey.github.io/shellter---the-ultimate-tool-for-av-evasion.html", "Hack like a Pro: Evade AV Software with Shellter": "https://null-byte.wonderhowto.com/how-to/hack-like-pro-evade-av-software-with-shellter-0168504/"})
def linux_private_i():
    os.system("clear")
    github = "A Linux Enumeration & Privilege Escalation tool that automates the basic enumeration steps and displays the results in an easily readable format. The script comes loaded with a variety of 4 Options to choose from. Using Bash, execute private-i.sh on the local low privileged user. Select an option, execute & watch the show. Each mode uses common Linux binaries to enumerate the local system (find, grep, ps, etc). If you have a non-bash shell such as sh, use Noir-Private-i. Either script will not write or auto-exploit in any way"
    template.template("linux-private-i", "./private-i.sh", github.strip(), {"Documentation": "https://github.com/rtcrowley/linux-private-i/blob/master/README.md", "HackingArticles-linux-privilege-escalation-automated-script":
                              "https://www.hackingarticles.in/linux-privilege-escalation-automated-script"}, method="github", github_install="git clone https://github.com/rtcrowley/linux-private-i.git && cd linux-private-i && chmod +x *", github_check="linux-private-i")
def pspy():
    os.system("clear")
    github = "pspy is a command line tool designed to snoop on processes without need for root permissions. It allows you to see commands run by other users, cron jobs, etc. as they execute. Great for enumeration of Linux systems in CTFs. Also great to demonstrate your colleagues why passing secrets as arguments on the command line is a bad idea.This tool gathers the info from procfs scans. Inotify watchers placed on selected parts of the file system trigger these scans to catch short-lived processes."
    version = github_getting_text("https://github.com/DominicBreuker/pspy/releases/",
                                          'div[class="css-truncate css-truncate-target"]', 0).strip()
    template.template("pspy64", "chmod u+x pspy64 && ./pspy64", github.strip(), {"Using-PSPY-To-Monitor-Linux-Processes": "https://infinitelogins.com/2020/09/04/using-ps-py-to-monitor-linux-processes", "Cyberkendra Pspy-Tool-Monitor-Linux-Processes": "https://tools.cyberkendra.com/2020/04/pspy-tool-monitor-linux-processes.html", "How-To-Enumerate-Services-In-Use-With-PSPY": "https://vk9-sec.com/how-to-enumerate-services-in-use-with-pspy",
                              "TryHackMe-ConvertMyVideo Writeup": "https://sparshjazz.medium.com/tryhackme-convertmyvideo-writeup-56b6c8217001", "SecurityOnline PSPY": "https://securityonline.info/pspy"}, method="github", github_install=f"wget  https://github.com/DominicBreuker/pspy/releases/download/{version}/pspy64 && mkdir PSPY && mv pspy64 PSPY", github_check="PSPY")
def linux_smart_enumeration():
    os.system("clear")
    github = "Linux Smart Enumeration (LSE) is a script written by Diego Treitos that automates the enumeration process for Linux systems. It is designed to run quickly and efficiently, and to provide detailed information about the system, including users, groups, permissions, network configuration, and more. LSE is intended to be used by penetration testers and security professionals to gather information about a target system during the reconnaissance phase of an engagement."
    template.template("linux-smart-enumeration", "chmod u+x lse.sh && ./lse.sh", github.strip(), {"Documentation (linux-smart-enumeration)": "https://github.com/diego-treitos/linux-smart-enumeration/blob/master/README.md", "Use-Linux-Smart-Enumeration-Discover-Paths-Privesc":
                              "https://null-byte.wonderhowto.com/how-to/use-linux-smart-enumeration-discover-paths-privesc-0330807", "Hakin9 linux-smart-enumeration": "https://hakin9.org/linux-smart-enumeration"}, method="github", github_install="git clone https://github.com/diego-treitos/linux-smart-enumeration.git", github_check="linux-smart-enumeration")
def linux_exploit_suggester2():
    os.system("clear")
    github = "Linux Exploit Suggester 2 (LES 2) is a tool that can be used to identify potential vulnerabilities and exploits that can be used to compromise a Linux system. It works by analyzing the running kernel version and system information, and then comparing it to a local database of known vulnerabilities and exploits. LES 2 can also be used to determine whether a patch has been applied to a specific vulnerability, making it useful for identifying systems that are still vulnerable to known exploits. The tool is open-source and can be easily installed on a Linux system. It supports a wide range of Linux distributions, including Ubuntu, Debian, Fedora, Arch Linux and more. LES 2 is a command-line tool and requires Python to run.It's a useful tool for penetration testers and system administrators to identify and prioritize vulnerabilities on their systems."
    template.template("linux-exploit-suggester-2", "chmod u+x linux-exploit-suggester-2.pl && ./linux-exploit-suggester-2.pl", github.strip(), {"Kali Tools (linux-exploit-suggester)": "https://www.kali.org/tools/linux-exploit-suggester/", "Find-Exploits-Get-Root-With-Linux-Exploit-Suggester": "https://null-byte.wonderhowto.com/how-to/find-exploits-get-root-with-linux-exploit-suggester-0206005", "Pentest-Monkey Linux-Exploit-Suggester": "https://pentestmonkey.net/tools/audit/exploit-suggester",
                              "Linux-Exploit-Suggester-A-Kali-Linux-Tool-To-Find-The-Linux-Os-Kernel-Exploits": "https://gbhackers.com/linux-exploit-suggester-a-kali-linux-tool-to-find-the-linux-os-kernel-exploits", "Securityonline Linux-Exploit Suggester": "https://securityonline.info/linux-exploit-suggester-2"}, method="github", github_install="git clone https://github.com/jondonas/linux-exploit-suggester-2.git", github_check="linux-exploit-suggester-2")
def beroot():
    os.system("clear")
    github_text_0 = github_getting_text(
                "https://github.com/AlessandroZ/BeRoot", 'p[dir=auto]', 0)
    github_text_1 = github_getting_text(
                "https://github.com/AlessandroZ/BeRoot", 'p[dir=auto]', 1)
    github = github_text_0.strip().replace("\n", "").replace("\t", "") + github_text_1.strip().replace("\n", "").replace("\t", "")
    template.template("BeRoot", "cd Linux && chmod u+x * && ./beroot.py", github.strip(), {"BeRoot-Linux-Privilege-Escalation": "https://www.kitploit.com/2018/06/beroot-for-linux-privilege-escalation.html?m=0", "BeRoot-A-Post-Exploitation-Privilege-Escalation-Tool":
                              "https://blog.hackersonlineclub.com/2018/07/beroot-post-exploitation-tool-to-check.html", "BeRoot-Windows-Privilege-Escalation": "https://sevenlayers.com/index.php/273-windows-privilege-escalation"}, method="github", github_install="git clone https://github.com/AlessandroZ/BeRoot.git", github_check="BeRoot")
def sudokiller():
    os.system("clear")
    github_text_6 = github_getting_text(
                "https://github.com/TH3xACE/SUDO_KILLER", 'p[dir=auto]', 6)
    github_text_7 = github_getting_text(
                "https://github.com/TH3xACE/SUDO_KILLER", 'p[dir=auto]', 7)
    github = github_text_6 + github_text_7
    template.template("Sudo Killer", "chmod u+x * && ./SUDO_KILLERv3.sh", github.strip(), {"SUDO_KILLER-Demos": "https://github.com/TH3xACE/SUDO_KILLER#demos", "Sudo-Killer Information": "https://www.kitploit.com/2020/02/sudokiller-tool-to-identify-and-exploit.html",
                              "Sudo-Killer-Identify-Abuse-Sudo-Misconfigurations": "https://null-byte.wonderhowto.com/how-to/use-sudo-killer-identify-abuse-sudo-misconfigurations-0202594"}, method="github", github_install="git clone https://github.com/TH3xACE/SUDO_KILLER.git", github_check="SUDO_KILLER")
def linenum():
    os.system("clear")
    github = "LinEnum is a Linux enumeration script that can be used to enumerate information from a Linux system. It is designed to be run locally on a Linux system and will attempt to enumerate common files, folders, users, groups, services, configurations, and permissions. It can also be used to look for certain security vulnerabilities such as local privilege escalation. LinEnum can be run from the command line or can be automated using a script. The output of the script can be saved as a text file for later analysis."
    template.template("LinEnum", "chmod +x LinEnum.sh && ./LinEnum.sh -h", github.strip(), {"Use-LinEnum-Identify-Potential-Privilege-Escalation-Vectors": "https://null-byte.wonderhowto.com/how-to/use-linenum-identify-potential-privilege-escalation-vectors-0197225/", "Linux-Privilege-Escalation-With-LinEnum": "https://trevorxcohen.medium.com/linux-privilege-escalation-with-linenum-75d20a3b59f6", "LinEnum-Linux-Enumeration-Privilege-Escalation-Tool": "https://www.darknet.org.uk/2014/11/linenum-linux-enumeration-privilege-escalation-tool",
                              "Linux-Privilege-Escalation-Quick-And-Dirty": "https://reboare.gitbooks.io/booj-security/content/general-linux/privilege-escalation.html", "Linux Enumeration And Privilege Escalation – LinEnum": "https://vulners.com/n0where/N0WHERE:24819"}, method="github", github_install="curl -s https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -o LinEnum.sh && mkdir LinEnum && mv LinEnum.sh LinEnum", github_check="LinEnum")
def linpeas():
    os.system("clear")
    github = "LinPeas is a script that automates the process of gathering information about a Linux system, similar to Windows' PowerShell script PEAS. This script can help identify potential vulnerabilities and misconfigurations on a Linux system, as well as provide information about system and network configuration. It can be useful for penetration testing, security assessments, and incident response. The script can be executed with arguments to specify which information to gather, or without arguments to gather all available information"
    template.template("linPEAS", "chmod +x linpeas.sh && ./linpeas.sh -h", github.strip(), {"LinPeas Blog": "https://blog.cyberethical.me/linpeas", "Linux-Privilege-Escalation": "https://delinea.com/blog/linux-privilege-escalation", "Linux Privilege Escalation: Quick and Dirty": " https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS", "Outrunsec LinPeas":
                              "https://outrunsec.com/tag/linpeas/", "Linux-Privilege-Escalation-Suid-Binaries": "https://steflan-security.com/linux-privilege-escalation-suid-binaries"}, method="github", github_install="wget https://github.com/carlospolop/PEASS-ng/releases/latest/download/linpeas.sh  && mkdir LinPeas && mv linpeas.sh LinPeas", github_check="LinPeas")
if __name__ == '__main__':
    main()