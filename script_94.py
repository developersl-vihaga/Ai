import whois, argparse, sys, dns.resolver
from datetime import datetime
def is_registered(domain):
    try: 
        info = whois.whois(domain)
    except Exception:
        return False
    else:
        return bool(info.domain)
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain")
    args = parser.parse_args()
    domain = args.domain
    print("\n" + "-"*45)
    print("Gathering DNS info for: ", domain)
    print("Time started: " + str(datetime.now()))
    print("-"*45 + "\n")
    is_registered(domain)
    if is_registered(domain):
        print(domain, "is registered\n")
        info = whois.whois(domain)
        print("Domain registrar: ", info.registrar)
        print("WHOIS server: ", info.whois_server)
        print("Domain creation date: ", info.reation_date)
        print("Expiration date: ", info.expiration_date)
        print("\nALL INFO:\n")
        print(info)
    else:
        print(domain, "is not registered")
        sys.exit()