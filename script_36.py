from main.tools import (
    banner,
    colors,
    information_gathering,template
)
from main.tools import (
    Configuration_Management,
    Secure_Transmission,
    Authentication,
    Session_Management,
    Authorization,
    data_validation,
    Cryptography,
    File_Upload,
    RiskyFuncPayment,
    html5,
    dos
)
import os
import requests
from bs4 import BeautifulSoup
def main():
    while True:
        os.system("clear")
        banner.main()
        banner.attack("Pentesting and Bug Bounty")
        list_attacks = [
            " Information Gathering",
            " Configuration Management",
            " Secure Transmission",
            " Authentication",
            " Session Management",
            " Authorization",
            " Data Validation",
            " Denial of Service(DOS)",
            " Business Logic",
            "Cryptography",
            "Risky Functionality - File Uploads",
            "Risky Functionality - Card Payment",
            "HTML 5",
            "Go Back",
        ]
        for i in range(len(list_attacks)):
            print(colors.options, f"{i+1}) {list_attacks[i]}".title(), colors.reset)
        try:
            option = input(f"\n {colors.select}Select An Option ->{colors.reset}  ")
        except KeyboardInterrupt:
            return
        if option == "1":
            print("\n[+] Information Gathering")
            os.system("clear")
            information_gathering.main()
        elif option == "2":
            print("\n[+] Configuration Management")
            os.system("clear")
            Configuration_Management.main()
        elif option == "3":
            print("\n[+] Secure Transmission")
            os.system("clear")
            Secure_Transmission.main()
        elif option == "4":
            print("\n[+] Authentication")
            os.system("clear")
            Authentication.main()
        elif option == "5":
            print("\n[+] Session Management")
            os.system("clear")
            Session_Management.main()
        elif option == "6":
            print("\n[+] Authorization")
            os.system("clear")
            Authorization.main()
        elif option == "7":
            print("\n[+] Data Validation")
            os.system("clear")
            data_validation.main()
        elif option == "8":
            print("\n[+] Denial of Service")
            os.system("clear")
            dos.main()
        elif option == "9":
            print("\n[+] Business Logic")
            os.system("clear")
            template.template("Business Logic","no-tools",'Business logic is the custom rules or algorithms that handle the exchange of information between a database and user interface. Business logic is essentially the part of a computer program that contains the information (in the form of business rules) that defines or constrains how a business operates. Such business rules are operational policies that are usually expressed in true or false binaries. Business logic can be seen in the workflows that they support, such as in sequences or steps that specify in detail the proper flow of information or data, and therefore decision-making. Business logic is also known as "domain logic."',{"Business Logic":"https://portswigger.net/web-security/logic-flaws/examples#top","Exploiting Business Logic Vulnerabilities":"https://medium.com/armourinfosec/exploiting-business-logic-vulnerabilities-234f97d6c4c0","WEB APPLICATION — BUSINESS LOGIC VULNERABILITIES":"https://infosecwriteups.com/web-application-business-logic-vulnerabilities-51be9c6b99fa","Business Logic Flaw":"https://www.wallarm.com/what/business-logic-flaw"})
        elif option == "10":
            print("\n[+] Cryptography")
            os.system("clear")
            Cryptography.main()
        elif option == "11":
            print("\n[+] Risky Functionality - File Uploads")
            os.system("clear")
            File_Upload.main()
        elif option == "12":
            print("\n[+] Risky Functionality - Card Payment")
            os.system("clear")
            RiskyFuncPayment.main()
        elif option == "13":
            print("\n[+] HTML 5")
            os.system("clear")
            html5.main()
        else:
            return
def github_getting_text(link, selector, indexvalue):
    print("Please Wait....\r", end="")
    URL = link
    try:
        r = requests.get(URL)
        soup = BeautifulSoup(r.content, "html.parser")
        paras = soup.select(selector)
        return paras[indexvalue].text
    except:
        return f"{colors.red}Not Loaded Because No Internet Connection{colors.reset}"
if __name__ == "__main__":
    main()