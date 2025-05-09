from main.tools import banner, colors, template
import os
import requests
from bs4 import BeautifulSoup
def main():
    while True:
        os.system("clear")
        banner.main()
        banner.attack("Exploitation Tools")
        list_attacks = [" Metasploit\t\t(Recommended)", " CrackMapExec", " Searchsploit\t(Recommended)", " BeEF\t\t(Recommended)",
                        " RouterSploit", " Sqlmap\t\t(Recommended)", " Seclists\t\t(Recommended)", " Armitage", " Go Back"]
        for i in range(len(list_attacks)):
            print(colors.options, f"{i+1}) {list_attacks[i]}".title(), colors.reset)
        try:
            option = input(
                f"\n {colors.select}Select An Option ->{colors.reset}  ")
        except KeyboardInterrupt:
            return
        if option == "1":
            print("\n[+] Metasploit-Framework")
            metasploit()
        elif option == "2":
            print("\n[+] crackmapexec")
            crackmapexec()
        elif option == "3":
            print("\n[+] Searchsploit")
            searchsploit()
        elif option == "4":
            print("\n[+] beef")
            beef()
        elif option == "5":
            print("\n[+] RouterSploit")
            routersploit()            
        elif option == "6":
            print("\n[+] sqlmap")
            sqlmap()
        elif option == "7":
            print("\n[+] seclists")
            seclists()    
        elif option == "8":
            print("\n[+] Armitage")
            armitage()        
        else:
            return
def github_getting_text(link, selector, indexvalue):
    print("Please Wait....\r", end="")
    URL = link
    try:
        if selector=="p" and "github" in link:
            selector="p[dir=auto]"
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, 'html.parser')
        paras = soup.select(selector)
        return paras[indexvalue].text
    except:
        return f"{colors.red}Not Loaded Because No Internet Connection{colors.reset}"
def searchsploit():
    github = "The Exploit Database is an archive of public exploits and corresponding vulnerable software, developed for use by penetration testers and vulnerability researchers. Its aim is to serve as the most comprehensive collection of exploits, shellcode and papers gathered through direct submissions, mailing lists, and other public sources, and present them in a freely-available and easy-to-navigate database."
    template.template("exploitdb", "searchsploit", github.strip(), {"How to install Searchsploit": "https://www.exploit-db.com/searchsploit", "How to Use SearchSploit": "https://www.kali.org/tools/exploitdb/#searchsploit", "Finding Exploit offline using Searchsploit in Kali Linux":
                              "https://www.geeksforgeeks.org/finding-exploit-offline-using-searchsploit-in-kali-linux/", "How to easy find exploits with Searchsploit on Linux": "https://medium.com/@hninja049/how-to-easy-find-exploits-with-searchsploit-on-linux-4ce0b82c82fd"})
def routersploit():
    os.system("clear")
    github = "The RouterSploit Framework is an open-source exploitation framework dedicated to embedded devices. It consists of various modules that aid penetration testing operations: exploits - modules that take advantage of identified vulnerabilities. creds - modules designed to test credentials against network services."
    template.template("routersploit", "routersploit", github.strip(), {"How to Use Routersploit": "https://www.kali.org/tools/routersploit/",
                              "Routersploit Tutorial": "https://kalitut.com/routersploit/", "RouterSploit User Manual": "https://miloserdov.org/?p=1527"})
def seclists():
    os.system("clear")
    github = github_getting_text(
            "https://github.com/danielmiessler/SecLists", 'p', 1)
    template.template("seclists", "seclists", github.strip(), {
                              "Using SecLists for Penetration Testing": "https://www.varutra.com/using-seclists-for-penetration-testing/"},)
def armitage():
    os.system("clear")
    github = "Armitage is a fantastic Java-based GUI front-end for the Metasploit Framework developed by Raphael Mudge. Its goal is to help security professionals better understand hacking and help them realize the power and potential of Metasploit."
    template.template("armitage", "armitage", github.strip(), {"How to Install Armitage on Kali Linux": "https://linuxhint.com/install-armitage-kali-linux/",
                              "Armitage Setup": "https://www.offensive-security.com/metasploit-unleashed/armitage-setup/", "Hacking With Armitage on Kali Linux / Backtrack ": "https://www.amirootyet.com/post/hacking-with-armitage-on-kali-linux/"})
def metasploit():
    os.system("clear")
    github = "The Metasploit Framework is an open-source tool for developing and executing exploit code against a remote target machine. It can be used to test the security of a computer system by finding and exploiting vulnerabilities. The framework includes a large collection of exploit modules, as well as various tools for payload generation, post-exploitation, and more. It can be used by security professionals for penetration testing, as well as by attackers for malicious purposes."
    template.template("metasploit-framework", "msfconsole", github.strip(), {" Msf-Community-Post-Exploitation": "https://www.offensive-security.com/metasploit-unleashed/msf-community-post-exploitation", " Post Exploitation In Linux With Metasploit": "https://pentestlab.blog/2013/01/04/post-exploitation-in-linux-with-metasploit/", " Privilege Escalation (Metasploit Unleashed)": "https://www.offensive-security.com/metasploit-unleashed/privilege-escalation/", " Post Exploitation Metasploit Modules (Reference)": "https://www.infosecmatter.com/post-exploitation-metasploit-modules-reference", " PSExec Pass the Hash (Horizontal Escalation)": "https://www.offensive-security.com/metasploit-unleashed/psexec-pass-hash/", " ms10_002_aurora (Vertical Escalation)": "https://www.offensive-security.com/metasploit-unleashed/privilege-escalation/", " ms10_002_aurora (Horizontal Escalation)": "https://www.offensive-security.com/metasploit-unleashed/pivoting/ ", " jtr_crack_fast (Hash Cracking)": "https://www.offensive-security.com/metasploit-unleashed/john-ripper/", " warftpd_165_user (Keylogging)":
                      "https://www.offensive-security.com/metasploit-unleashed/keylogging/", "3proxy (Backdoor)": "https://www.offensive-security.com/metasploit-unleashed/meterpreter-backdoor/", "persistence.rb (Persistent Backdoor)": "https://www.offensive-security.com/metasploit-unleashed/meterpreter-service/", "Enabling Remote Desktop": "https://www.offensive-security.com/metasploit-unleashed/enabling-remote-desktop/", "Hack Like Pro: Kill and Disable Antivirus Software Remote PC": "https://null-byte.wonderhowto.com/how-to/hack-like-pro-kill-and-disable-antivirus-software-remote-pc-0141906/", "Armitage Post Exploitation": "https://www.offensive-security.com/metasploit-unleashed/armitage-post-exploitation/", "Setup Armitage as a Command & Control Framework for Free": "https://infosecwriteups.com/setup-armitage-as-a-command-control-c2-framework-for-free-bae590064817", "Event Log Management": "https://www.offensive-security.com/metasploit-unleashed/event-log-management", "Interacting with the Registry": "https://www.offensive-security.com/metasploit-unleashed/interacting-registry"})
def sqlmap():
    os.system("clear")
    github = "sqlmap is an open source penetration testing tool that automates the process of detecting and exploiting SQL injection flaws and taking over of database servers. It comes with a powerful detection engine, many niche features for the ultimate penetration tester and a broad range of switches lasting from database fingerprinting, over data fetching from the database, to accessing the underlying file system and executing commands on the operating system via out-of-band connections"
    template.template("sqlmap", "sqlmap -h", github.strip(), {"Usage Of Sqlmap": "https://github.com/sqlmapproject/sqlmap/wiki/Usage", "How to use SQLMAP to test a website for SQL Injection vulnerability": "https://www.geeksforgeeks.org/use-sqlmap-test-website-sql-injection-vulnerability/",
                      "How to Use SQLMap to Find Database Vulnerabilities": "https://www.freecodecamp.org/news/how-to-protect-against-sql-injection-attacks/", "SQLMap - Cheetsheat": "https://book.hacktricks.xyz/pentesting-web/sql-injection/sqlmap"})
def crackmapexec():
    os.system("clear")
    github = "CrackMapExec (a.k.a CME) is a post-exploitation tool that helps automate assessing the security of large Active Directory networks. Built with stealth in mind, CME follows the concept of Living off the Land : abusing built-in Active Directory features/protocols to achieve it's functionality and allowing it to evade most endpoint protection/IDS/IPS solutions."
    template.template("crackmapexec", "crackmapexec", github.strip(), {"CrackMapExec in Kali Linux": "https://www.kali.org/tools/crackmapexec/", "How to Use CrackMapExec": "https://bond-o.medium.com/crackmapexec-basics-839ef6180940",
                      "Lateral Movement on Active Directory: CrackMapExec": "https://www.hackingarticles.in/lateral-moment-on-active-directory-crackmapexec/", "CrackMapExec Cheat sheet": "https://cheatsheet.haax.fr/windows-systems/exploitation/crackmapexec/"})
def beef():
    os.system("clear")
    github_p1 = github_getting_text("https://beefproject.com/", 'p', 0)
    github_p2 = github_getting_text("https://beefproject.com/", 'p', 1)
    github = github_p1.strip().replace("\n", "").replace("\t", "")+github_p2.strip().replace("\n", "").replace("\t", "")
    template.template("beef-xss", "beef-xss", github.strip(), {"BEeF Hacking Framework Tutorial [5 Easy Steps]": "https://www.golinuxcloud.com/beef-hacking-framework-tutorial/", "Browser Exploitation and Advanced Threat Actors: An Overview of BeEF": "https://medium.com/@andrearebora/browser-exploitation-and-advanced-threat-actors-an-overview-of-beef-bb907a5b73fa",
                      "Hooking victims to Browser Exploitation Framework (BeEF) using Reflected and Stored XSS.": "https://medium.com/@secureica/hooking-victims-to-browser-exploitation-framework-beef-using-reflected-and-stored-xss-859266c5a00a", "Hijacking Browser with BeEF Framework": "https://medium.com/@krunalkumarpatel/hijacking-browser-with-beef-framework-bea784c03149"})
if __name__ == '__main__':
    main()