import threading
from threading import enumerate
from sys import exit
from impacket import smbserver
class CMESMBServer(threading.Thread):
    def __init__(
        self,
        logger,
        share_name,
        share_path="/tmp/cme_hosted",
        listen_address="0.0.0.0",
        listen_port=445,
        verbose=False,
    ):
        try:
            threading.Thread.__init__(self)
            self.server = smbserver.SimpleSMBServer(listen_address, listen_port)
            self.server.addShare(share_name.upper(), share_path)
            if verbose:
                self.server.setLogFile("")
            self.server.setSMB2Support(True)
            self.server.setSMBChallenge("")
        except Exception as e:
            errno, message = e.args
            if errno == 98 and message == "Address already in use":
                logger.error("Error starting SMB server on port 445: the port is already in use")
            else:
                logger.error(f"Error starting SMB server on port 445: {message}")
                exit(1)
    def addShare(self, share_name, share_path):
        self.server.addShare(share_name, share_path)
    def run(self):
        try:
            self.server.start()
        except:
            pass
    def shutdown(self):
        for thread in enumerate():
            if thread.is_alive():
                try:
                    self._stop()
                except:
                    pass