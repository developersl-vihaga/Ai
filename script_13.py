import os
import requests
from main.tools import banner, colors, template, information_gathering, WEB_Application_Analysis
from bs4 import BeautifulSoup
def main():
    while True:
        os.system("clear")
        banner.main()
        banner.attack("Vulnerability Analysis")
        list_attacks = ["Wpscan\t\t(Recommended)", "Wireshark\t\t(Recommended)",
                        "Wapiti", "Nmap\t\t(Recommended)", "Legion", "Nikto", "Wfuzz", "go back"]
        for i in range(len(list_attacks)):
            print(colors.options, f"{i+1}) {list_attacks[i]}".title(), colors.reset)
        try:
            option = input(
                f"\n {colors.select}Select An Option ->{colors.reset}  ")
        except KeyboardInterrupt:
            return
        if option == "1":
            print("\n[+] Wpscan")
            wpscan()
        elif option == "2":
            print("\n[+] Wireshark")
            wireshark()
        elif option == "3":
            print("\n[+] Wapiti")
            WEB_Application_Analysis.wapiti()
        elif option == "4":
            print("\n[+] Nmap")
            information_gathering.nmap()
        elif option == "5":
            print("\n[+] legion")
            legion()
        elif option == "6":
            print("\n[+] Nikto")
            nikto()
        elif option == "7":
            print("\n[+] Wfuzz")
            wfuzz()
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
        return f"{colors.red}NotLloaded Because No Internet Connection{colors.reset}"
def tool_writeups():
    print(f"{colors.options}1) TOOL(About,Installation)")
    print(f"2) Write Ups")
    print(f"3) Go Back..")
    try:
        ask = input(f"\n {colors.select}Select An Option ->{colors.reset}  ")
    except KeyboardInterrupt:
        return
    return ask
def wfuzz():
    os.system("clear")
    github = "Wfuzz is a web application brute force tool used to identify web application vulnerabilities by scanning web content, such as directories and files, for hidden or non-linked content. Wfuzz can be used to test input validation, error handling, and access control mechanisms. It is a command-line tool and allows users to customize requests to send payloads, which makes it very flexible and powerful for web application penetration testing. Wfuzz is written in Python and can be used on Linux, Windows, and macOS. It is open-source and free to use."
    template.template(
                "wfuzz", "wfuzz --help", github.strip(), {"How to use Wfuzz to find web application vulnerabilities":
                                                          "https://www.techtarget.com/searchsecurity/feature/How-to-use-Wfuzz-to-find-web-application-vulnerabilities", }
            )
def wireshark():
    os.system("clear")
    github = "Wireshark is a network traffic analyzer, or sniffer, for Linux, macOS, BSD and other Unix and Unixlike operating systems and for Windows. It uses Qt, a graphical user interface library, and libpcap and npcap as packet capture and filtering libraries."
    template.template("wireshark", "wireshark", github.strip(), {'How To Install & Use Wireshark On Kali Linux': 'https://infosecscout.com/wireshark-on-kali-linux/', 'Wireshark Tool Documentation': 'https://www.kali.org/tools/wireshark/', 'Wireshark Training': 'https://www.wireshark.org/docs/', 'Wireshark – Resources': 'https://blog.inf.ed.ac.uk/atate/2023/01/14/wireshark-resources/',
                              'Kerberos Wireshark Captures: A Windows Login Example': 'https://medium.com/@robert.broeckelmann/kerberos-wireshark-captures-a-windows-login-example-151fabf3375a', 'Wireshark – Packet Capturing and Analyzing': 'https://www.geeksforgeeks.org/wireshark-packet-capturing-and-analyzing/', 'Wireshark Tutorial: Decrypting HTTPS Traffic': 'https://unit42.paloaltonetworks.com/wireshark-tutorial-decrypting-https-traffic/'})
def legion():
    os.system("clear")
    github = github_getting_text(
        "https://github.com/GoVanguard/legion", 'p[class="f4 my-3"]', 0)
    template.template("legion", "legion", github.strip(), {"Legion: The best all in one network mapping tool": "https://techyrick.com/legion-kali-linux/", "An Overview Of Network Penetration Testing Using Legion Framework": "https://www.c-sharpcorner.com/article/an-overview-of-network-penetration-testing-using-legion-framework/#:~:text=What%20is%20Legion%3F,the%20attacks%20against%20targeted%20devices.",
                      'Legion Tool in Kali Linux': 'https://www.geeksforgeeks.org/legion-tool-in-kali-linux', 'Legion -- Test Web Application Vulnerability Automatically': 'https://www.kalilinux.in/2020/09/legion-kali-linux.html', 'How to use Legion application in Kali Linux Video Tutorial': 'https://www.youtube.com/watch?v=0v2_UFhq6zQ'})
def nikto():
    os.system("clear")
    github = github_getting_text(
        "https://en.wikipedia.org/wiki/Nikto_(vulnerability_scanner)", 'p', 1)
    template.template("nikto", "nikto -h", github.strip(), {'What is Nikto and it’s usages ?': 'https://www.geeksforgeeks.org/what-is-nikto-and-its-usages/',
                      'Nikto: A Practical Website Vulnerability Scanner': 'https://securitytrails.com/blog/nikto-website-vulnerability-scanner', 'Nikto Official Docs': 'https://github.com/sullo/nikto/wiki'})
def wpscan():
    os.system("clear")
    github = "WPScan is a security scanner designed for testing the security of websites built using WordPress. WPScan was developed using the Ruby programming language and then released in the first version in 2019. The WPScan security scanner is primarily intended to be used by WordPress administrators and security teams to assess the security status of their WordPress installations. It is used to scan WordPress websites for known vulnerabilities both in WordPress and commonly used WordPress plugins and themes. The code base for WPScan is licensed under GPLv3"
    template.template("wpscan", "wpscan -h", github.strip(), {'WPScan Intro: How to Scan for WordPress Vulnerabilities': 'https://blog.sucuri.net/2021/05/wpscan-how-to-scan-for-wordpress-vulnerabilities.html/', 'WPScan:WordPress Pentesting Framework': 'https://www.hackingarticles.in/wpscanwordpress-pentesting-framework/', 'How To Use WPScan to Test for Vulnerable Plugins and Themes in Wordpress':
                      "https://www.digitalocean.com/community/tutorials/how-to-use-wpscan-to-test-for-vulnerable-plugins-and-themes-in-wordpress", "How to Use wpscan tool in Kali Linux": "https://www.geeksforgeeks.org/how-to-use-wpscan-tool-in-kali-linux/", "WPScan Usage Example [Enumeration + Exploit]": "https://www.cyberpunk.rs/wpscan-usage-example"})
if __name__ == '__main__':
    main()