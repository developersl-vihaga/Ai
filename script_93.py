import dns.resolver, argparse
from datetime import datetime
def enumerate(domain):
    records = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
    resolver = dns.resolver.Resolver()
    for record in records:
        try:
            answer = resolver.resolve(domain, record)
        except dns.resolver.NoAnswer:
            continue
        print(f"\n{record} records for {domain}:")
        for record_data in answer:
            print(f"{record_data}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--domain")
    args = parser.parse_args()
    domain = args.domain
    print("\n" + "-"*45)
    print("Gathering DNS info for: ", domain)
    print("Time started: " + str(datetime.now()))
    print("-"*45 + "\n")
    enumerate(domain)