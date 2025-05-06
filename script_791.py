import sys, time
from cme.logger import CMEAdapter
from bloodhound.ad.domain import ADDC
from bloodhound.enumeration.computers import ComputerEnumerator
from bloodhound.enumeration.memberships import MembershipEnumerator
from bloodhound.enumeration.domains import DomainEnumerator
class BloodHound(object):
    def __init__(self, ad, hostname, host, port):
        self.ad = ad
        self.ldap = None
        self.pdc = None
        self.sessions = []
        self.hostname = hostname
        self.dc = hostname
        self.proto_logger(port, hostname, host)
    def proto_logger(self, port, hostname, host):
        self.logger = CMEAdapter(extra={"protocol": "LDAP", "host": host, "port": port, "hostname": hostname})
    def connect(self):
        if len(self.ad.dcs()) == 0:
            self.logger.fail("Could not find a domain controller. Consider specifying a domain and/or DNS server.")
            sys.exit(1)
        if not self.ad.baseDN:
            self.logger.fail("Could not figure out the domain to query. Please specify this manually with -d")
            sys.exit(1)
        pdc = self.ad.dcs()[0]
        self.logger.debug("Using LDAP server: %s", pdc)
        self.logger.debug("Using base DN: %s", self.ad.baseDN)
        if len(self.ad.kdcs()) > 0:
            kdc = self.ad.kdcs()[0]
            self.logger.debug("Using kerberos KDC: %s", kdc)
            self.logger.debug("Using kerberos realm: %s", self.ad.realm())
        self.pdc = ADDC(pdc, self.ad)
        self.ad.create_objectresolver(self.pdc)
    def run(
        self,
        collect,
        num_workers=10,
        disable_pooling=False,
        timestamp="",
        computerfile="",
        cachefile=None,
        exclude_dcs=False,
    ):
        start_time = time.time()
        if cachefile:
            self.ad.load_cachefile(cachefile)
        do_computer_enum = any(
            method in collect
            for method in [
                "localadmin",
                "session",
                "loggedon",
                "experimental",
                "rdp",
                "dcom",
                "psremote",
            ]
        )
        if "group" in collect or "objectprops" in collect or "acl" in collect:
            self.pdc.prefetch_info(
                "objectprops" in collect,
                "acl" in collect,
                cache_computers=do_computer_enum,
            )
            membership_enum = MembershipEnumerator(self.ad, self.pdc, collect, disable_pooling)
            membership_enum.enumerate_memberships(timestamp=timestamp)
        elif "container" in collect:
            self.pdc.prefetch_info(
                "objectprops" in collect,
                "acl" in collect,
                cache_computers=do_computer_enum,
            )
            membership_enum = MembershipEnumerator(self.ad, self.pdc, collect, disable_pooling)
            membership_enum.do_container_collection(timestamp=timestamp)
        elif do_computer_enum:
            self.pdc.prefetch_info("objectprops" in collect, "acl" in collect, cache_computers=True)
        elif "trusts" in collect:
            self.pdc.get_domains("acl" in collect)
        if "trusts" in collect or "acl" in collect or "objectprops" in collect:
            trusts_enum = DomainEnumerator(self.ad, self.pdc)
            trusts_enum.dump_domain(collect, timestamp=timestamp)
        if do_computer_enum:
            have_gc = len(self.ad.gcs()) > 0
            computer_enum = ComputerEnumerator(
                self.ad,
                self.pdc,
                collect,
                do_gc_lookup=have_gc,
                computerfile=computerfile,
                exclude_dcs=exclude_dcs,
            )
            computer_enum.enumerate_computers(self.ad.computers, num_workers=num_workers, timestamp=timestamp)
        end_time = time.time()
        minutes, seconds = divmod(int(end_time - start_time), 60)
        self.logger.highlight("Done in %02dM %02dS" % (minutes, seconds))