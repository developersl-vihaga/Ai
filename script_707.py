from ipaddress import ip_address
from impacket.dcerpc.v5 import transport
from impacket.dcerpc.v5.rpcrt import RPC_C_AUTHN_LEVEL_NONE
from impacket.dcerpc.v5.dcomrt import IObjectExporter
class CMEModule:
    name = "ioxidresolver"
    description = "This module helps you to identify hosts that have additional active interfaces"
    supported_protocols = ["smb", "wmi"]
    opsec_safe = True
    multiple_hosts = False
    def options(self, context, module_options):
        """ """
    def on_login(self, context, connection):
        authLevel = RPC_C_AUTHN_LEVEL_NONE
        stringBinding = r"ncacn_ip_tcp:%s" % connection.host
        rpctransport = transport.DCERPCTransportFactory(stringBinding)
        portmap = rpctransport.get_dce_rpc()
        portmap.set_auth_level(authLevel)
        portmap.connect()
        objExporter = IObjectExporter(portmap)
        bindings = objExporter.ServerAlive2()
        context.log.debug("[*] Retrieving network interface of " + connection.host)
        for binding in bindings:
            NetworkAddr = binding["aNetworkAddr"]
            try:
                ip_address(NetworkAddr[:-1])
                context.log.highlight("Address: " + NetworkAddr)
            except Exception as e:
                context.log.debug(e)