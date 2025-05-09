"""
SET core PyFakeMiniDNS server implementation.
Slightly modified implementation of Francisco Santos's PyfakeminiDNS
script designed to run as a thread and handle various additional
system configuration tasks, if necessary in the running environment,
along with a few implementation considerations specifically for SET.
"""
import os
import socket
import subprocess
import sys
import threading
dns_server_thread = None
def start_dns_server(reply_ip):
    """
    Helper function, intended to be called from other modules.
    Args:
        reply_ip (string): IPv4 address in dotted quad notation to use in all answers.
    """
    global dns_server_thread
    dns_server_thread = MiniFakeDNS(kwargs={'port': 53, 'ip': reply_ip})
    dns_server_thread.start()
def stop_dns_server():
    """
    Helper function, intended to be called from other modules.
    """
    dns_server_thread.stop()
    dns_server_thread.join()
    dns_server_thread.cleanup()
class DNSQuery:
    """
    A DNS query (that can be parsed as binary data).
    See original for reference, but note there have been changes:
        https://code.activestate.com/recipes/491264-mini-fake-dns-server/
    Among the changes are variables names that have been translated
    to English from their original Spanish.
    """
    def __init__(self, data):
        """
        Args:
            data (bytes): The binary data of the DNS packet from the wire.
        """
        self.data = data
        self.domain = ''
        txn_id = data[:2]  # DNS transaction ID, two bytes.
        flags  = data[2:4] # DNS flags, also two bytes.
        kind = (flags[0] >> 3) & 31 # Opcode is in bits 4, 5, 6, and 7 of first byte.
        if 0 == kind:               # was a standard query.
            offset = 12 # The first question begins at the 13th byte.
            length = data[offset]
            while 0 != length:
                self.domain += data[offset + 1 : offset + length + 1].decode() + '.'
                offset += length + 1
                length = data[offset]
    def response(self, ip):
        """
        Construct a DNS reply packet with a given IP address.
        TODO: This responds incorrectly to EDNS queries that make use
              of the OPT pseudo-record type. Specifically, the pointer
              wrong because we do not check the length of the original
              query we received. Instead, we should note the length of
              the original packet until the end of the first question,
              and truncate (i.e., drop, ignore) the remainder.
              For now, what this actually means is that testing this
              server using a recent version of `dig(1)` will fail
              unless you use the `+noedns` query option. For example:
                  dig @127.0.0.1 example.com +noedns
              Simpler or older DNS utilities such as `host(1)` are
              probably going to work.
        Args:
            ip (string): IP address to respond with.
        """
        packet = b''
        if self.domain:
            packet += self.data[:2] + b'\x81\x80'
            packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00' # Questions and Answers Counts
            packet += self.data[12:]                                        # Original Domain Name Question
            packet += b'\xc0\x0c'                                           # Pointer to domain name
            packet += b'\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04' # Response type, ttl and resource data length -> 4 bytes
            packet += bytes([int(x) for x in ip.split('.')])      # 4 bytes of IP.
        return packet
class MiniFakeDNS(threading.Thread):
    """
    The MiniFakeDNS server, written to be run as a Python Thread.
    """
    def __init__(self, group=None, target=None, name=None,
                       args=(), kwargs=None):
        super(MiniFakeDNS, self).__init__(
                group=group, target=target, name=name)
        self.args = args
        self.kwargs = kwargs
        self.ip = kwargs['ip']
        self.port = kwargs['port']
        self.cede_configuration = None
        self.stop_flag = False
    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udps:
            udps.setblocking(False)
            try:
                udps.bind(('', self.port))
            except OSError as e:
                if 'Address already in use' == e.strerror and os.path.exists('/etc/resolv.conf'):
                    if 'stub-resolv.conf' in os.path.realpath('/etc/resolv.conf'):
                        self.usurp_systemd_resolved()
                        self.cede_configuration = self.cede_to_systemd_resolved
                    udps.bind(('', self.port))
            while not self.stop_flag:
                try:
                    data, addr = udps.recvfrom(1024)
                    p = DNSQuery(data)
                    udps.sendto(p.response(self.ip), addr)
                except BlockingIOError:
                    pass
            print("Exiting the DNS Server..")
        sys.exit()
    def cleanup(self):
        if self.cede_configuration is not None:
            self.cede_configuration()
    def stop(self):
        """
        Signals to the DNS server thread to stop.
        """
        self.stop_flag = True
    def usurp_systemd_resolved(self):
        """
        Helper function to get systemd-resolved out of the way when it
        is listening on 127.0.0.1:53 and we are trying to run SET's
        own DNS server.
        """
        try:
            os.mkdir('/etc/systemd/resolved.conf.d')
        except (OSError, FileExistsError):
            pass
        with open('/etc/systemd/resolved.conf.d/99-setoolkit-dns.conf', 'w') as f:
            f.write("[Resolve]\nDNS=9.9.9.9\nDNSStubListener=no")
        os.rename('/etc/resolv.conf', '/etc/resolv.conf.original')
        os.symlink('/run/systemd/resolve/resolv.conf', '/etc/resolv.conf')
        subprocess.call(['systemctl', 'restart', 'systemd-resolved.service'])
    def cede_to_systemd_resolved(self):
        """
        Helper function to cede system configuration back to systemd-resolved
        after we have usurped control over DNS configuration away from it.
        """
        os.remove('/etc/systemd/resolved.conf.d/99-setoolkit-dns.conf')
        os.remove('/etc/resolv.conf')
        os.rename('/etc/resolv.conf.original', '/etc/resolv.conf')
        subprocess.call(['systemctl', 'restart', 'systemd-resolved.service'])