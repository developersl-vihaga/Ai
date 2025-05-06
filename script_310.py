from lib.common import helpers
class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Dylib Hijack Vulnerability Scanner',
            'Author': ['@patrickwardle','@xorrior'],
            'Description': ('This module can be used to identify applications vulnerable to dylib hijacking on a target system. This has been modified from the original to remove the dependancy for the macholib library.'),
            'Background' : False,
            'OutputExtension' : None,
            'NeedsAdmin' : False,
            'OpsecSafe' : True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': [
                'Heavily adapted from @patrickwardle\'s script: https://github.com/synack/DylibHijack/blob/master/scan.py'
            ]
        }
        self.options = {
            'Agent' : {
                'Description'   :   'Agent to run the module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Path' : {
                'Description'   :   'Scan all binaries recursively, in a specific path.',
                'Required'      :   False,
                'Value'         :   ''
            },
            'LoadedProcesses' : {
                'Description'   :   'Scan only loaded process executables',
                'Required'      :   True,
                'Value'         :   'False'
            }
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        scanPath = self.options['Path']['Value']
        LoadedProcesses = self.options['LoadedProcesses']['Value']
        script = """
from ctypes import *
def run():
    import ctypes
    import os
    import sys
    import shlex
    import subprocess
    import io
    import struct
    from datetime import datetime
    SUPPORTED_ARCHITECTURES = ['i386', 'x86_64']
    LC_REQ_DYLD = 0x80000000
    LC_LOAD_WEAK_DYLIB = LC_REQ_DYLD | 0x18
    LC_RPATH = (0x1c | LC_REQ_DYLD)
    LC_REEXPORT_DYLIB = 0x1f | LC_REQ_DYLD
    (
        LC_SEGMENT, LC_SYMTAB, LC_SYMSEG, LC_THREAD, LC_UNIXTHREAD, LC_LOADFVMLIB,
        LC_IDFVMLIB, LC_IDENT, LC_FVMFILE, LC_PREPAGE, LC_DYSYMTAB, LC_LOAD_DYLIB,
        LC_ID_DYLIB, LC_LOAD_DYLINKER, LC_ID_DYLINKER, LC_PREBOUND_DYLIB,
        LC_ROUTINES, LC_SUB_FRAMEWORK, LC_SUB_UMBRELLA, LC_SUB_CLIENT,
        LC_SUB_LIBRARY, LC_TWOLEVEL_HINTS, LC_PREBIND_CKSUM
    ) = range(0x1, 0x18)
    MH_MAGIC = 0xfeedface
    MH_CIGAM = 0xcefaedfe
    MH_MAGIC_64 = 0xfeedfacf
    MH_CIGAM_64 = 0xcffaedfe
    _CPU_ARCH_ABI64  = 0x01000000
    CPU_TYPE_NAMES = {
        -1:     'ANY',
        1:      'VAX',
        6:      'MC680x0',
        7:      'i386',
        _CPU_ARCH_ABI64  | 7:    'x86_64',
        8:      'MIPS',
        10:     'MC98000',
        11:     'HPPA',
        12:     'ARM',
        13:     'MC88000',
        14:     'SPARC',
        15:     'i860',
        16:     'Alpha',
        18:     'PowerPC',
        _CPU_ARCH_ABI64  | 18:    'PowerPC64',
    }
    class mach_header(ctypes.Structure):
        _fields_ = [
            ("magic", ctypes.c_uint),
            ("cputype", ctypes.c_uint),
            ("cpusubtype", ctypes.c_uint),
            ("filetype", ctypes.c_uint),
            ("ncmds", ctypes.c_uint),
            ("sizeofcmds", ctypes.c_uint),
            ("flags", ctypes.c_uint)
        ]
    class mach_header_64(ctypes.Structure):
        _fields_ = mach_header._fields_ + [('reserved',ctypes.c_uint)]
    class load_command(ctypes.Structure):
        _fields_ = [
            ("cmd", ctypes.c_uint),
            ("cmdsize", ctypes.c_uint)
        ]
    MH_EXECUTE = 2
    MH_DYLIB = 6
    MH_BUNDLE = 8
    LC_Header_Sz = 0x8
    def isSupportedArchitecture(machoHandle):
        headersz = 28
        header64sz = 32
        supported = False
        header = ""
        try:
            magic = struct.unpack('<L',machoHandle.read(4))[0]
            cputype = struct.unpack('<L',machoHandle.read(4))[0]
            machoHandle.seek(0, io.SEEK_SET)
            if CPU_TYPE_NAMES.get(cputype) == 'i386':
                header = mach_header.from_buffer_copy(machoHandle.read(headersz))
                supported = True
            elif CPU_TYPE_NAMES.get(cputype) == 'x86_64':
                header = mach_header_64.from_buffer_copy(machoHandle.read(header64sz)) 
                supported = True
            else:
                header = None 
        except:
            pass
        return (supported, header)
    def loadedBinaries():
        binaries = []
        lsof = subprocess.Popen('lsof /', shell=True, stdout=subprocess.PIPE)
        output = lsof.stdout.read()
        lsof.stdout.close()
        lsof.wait()
        for line in output.split('\\n'):
            try:
                binary = ' '.join(shlex.split(line)[8:])
                if not os.path.isfile(binary) or not os.access(binary, os.X_OK):
                    continue
                binaries.append(binary)
            except:
                pass
        binaries = list(set(binaries))
        return binaries
    def installedBinaries(rootDirectory = None):
        binaries = []
        if not rootDirectory:
            rootDirectory = '/'
        for root, dirnames, filenames in os.walk(rootDirectory):
            for filename in filenames:
                fullName = os.path.realpath(os.path.join(root, filename))
                if not os.path.isfile(fullName):
                    continue
                if os.access(fullName, os.X_OK) and (os.path.splitext(fullName)[-1] == '.dyblib' or os.path.splitext(fullName)[-1] == ''):
                    binaries.append(fullName)
        print "Finished with installed binaries\\n"
        return binaries
    def resolvePath(binaryPath, unresolvedPath):
        resolvedPath = unresolvedPath
        if unresolvedPath.startswith('@loader_path'):
            resolvedPath = os.path.abspath(os.path.split(binaryPath)[0] + unresolvedPath.replace('@loader_path', ''))
        elif unresolvedPath.startswith('@executable_path'):
            resolvedPath = os.path.abspath(os.path.split(binaryPath)[0] + unresolvedPath.replace('@executable_path', ''))
        return resolvedPath
    def parseBinaries(binaries):
        parsedBinaries = {}
        for binary in binaries:
            try:
                f = open(binary, 'rb')
                if not f:
                    continue
            except:
                continue
            (isSupported, machoHeader) = isSupportedArchitecture(f)
            if not isSupported:
                continue
            if machoHeader.filetype not in [MH_EXECUTE, MH_DYLIB, MH_BUNDLE]:
                continue
            parsedBinaries[binary] = {'LC_RPATHs': [], 'LC_LOAD_DYLIBs' : [], 'LC_LOAD_WEAK_DYLIBs': [] }
            parsedBinaries[binary]['type'] = machoHeader.filetype
            if CPU_TYPE_NAMES.get(machoHeader.cputype) == 'x86_64':
                f.seek(32, io.SEEK_SET)
            else:
                f.seek(28, io.SEEK_SET) 
            for cmd in range(machoHeader.ncmds):
                try:
                    lc = load_command.from_buffer_copy(f.read(LC_Header_Sz))
                except Exception as e:
                    break #break out of the nested loop and continue with the parent loop
                size = lc.cmdsize
                if lc.cmd == LC_RPATH:
                    pathoffset = struct.unpack('<L',f.read(4))[0]
                    f.seek(pathoffset - (LC_Header_Sz + 4), io.SEEK_CUR)
                    path = f.read(lc.cmdsize - pathoffset)
                    rPathDirectory = path.rstrip('\\0')
                    rPathDirectory = resolvePath(binary, rPathDirectory)
                    parsedBinaries[binary]['LC_RPATHs'].append(rPathDirectory)
                elif lc.cmd == LC_LOAD_DYLIB:
                    pathoffset = struct.unpack('<L',f.read(4))[0]
                    f.seek(pathoffset - (LC_Header_Sz + 4), io.SEEK_CUR)
                    path = f.read(size - pathoffset)
                    importedDylib = path.rstrip('\\0')
                    parsedBinaries[binary]['LC_LOAD_DYLIBs'].append(importedDylib)
                elif lc.cmd == LC_LOAD_WEAK_DYLIB:
                    pathoffset = struct.unpack('<L',f.read(4))[0]
                    f.seek(pathoffset - (LC_Header_Sz + 4), io.SEEK_CUR)
                    path = f.read(size - pathoffset)
                    weakDylib = path.rstrip('\\0')
                    weakDylib = resolvePath(binary, weakDylib)
                    parsedBinaries[binary]['LC_LOAD_WEAK_DYLIBs'].append(weakDylib)
                else:
                    f.seek(size - LC_Header_Sz, io.SEEK_CUR)
        print "finished parsing load commands"
        return parsedBinaries
    def processBinaries(parsedBinaries):
        vulnerableBinaries = {'rpathExes': [], 'weakBins': []}
        for key in parsedBinaries:
            binary = parsedBinaries[key]
            if binary['type']== MH_EXECUTE and len(binary['LC_RPATHs']):
                for importedDylib in binary['LC_LOAD_DYLIBs']:
                    if not importedDylib.startswith('@rpath'):
                        continue
                    importedDylib = importedDylib.replace('@rpath', '')
                    if not os.path.exists(binary['LC_RPATHs'][0] + importedDylib):
                        vulnerableBinaries['rpathExes'].append({'binary': key, 'importedDylib': importedDylib, 'LC_RPATH': binary['LC_RPATHs'][0]})
                        break
            for weakDylib in binary['LC_LOAD_WEAK_DYLIBs']:
                if weakDylib.startswith('@rpath'):
                    if binary['type'] != MH_EXECUTE:
                        continue
                    if not len(binary['LC_RPATHs']):
                        continue
                    weakDylib = weakDylib.replace('@rpath', '')
                    if not os.path.exists(binary['LC_RPATHs'][0] + weakDylib):
                        vulnerableBinaries['weakBins'].append({'binary': key, 'weakDylib': weakDylib, 'LC_RPATH': binary['LC_RPATHs'][0]})
                        break
                elif not os.path.exists(weakDylib):
                    vulnerableBinaries['weakBins'].append({'binary': key, 'weakBin': weakDylib})
                    break
        return vulnerableBinaries
    path = "%s"
    ProcBinaries = "%s"
    startTime = datetime.now()
    if ProcBinaries.lower() == "true":
        binaries = loadedBinaries()
    elif path :
        binaries = installedBinaries(path)
    else:
        binaries = installedBinaries()
    parsedBinaries = parseBinaries(binaries)
    vulnerableBinaries = processBinaries(parsedBinaries)
    if len(vulnerableBinaries['rpathExes']):
        print '\\nfound %%d binaries vulnerable to multiple rpaths:' %% len(vulnerableBinaries['rpathExes'])
        for binary in vulnerableBinaries['rpathExes']:
            print '%%s has an rpath vulnerability: (%%s%%s)\\n' %% (binary['binary'], binary['LC_RPATH'],binary['importedDylib'])
    else:
        print '\\ndid not find any vulnerable to multiple rpaths'
    if len(vulnerableBinaries['weakBins']):
            print '\\nfound %%d binaries vulnerable to weak dylibs:' %% len(vulnerableBinaries['weakBins'])
            for binary in vulnerableBinaries['weakBins']:
                print '%%s has weak import (%%s)\\n' %% (binary['binary'], binary)
    else:
        print '\\ndid not find any missing LC_LOAD_WEAK_DYLIBs'
    print "Scan completed in " + str(datetime.now() - startTime) + "\\n"
    print "[+] To abuse an rpath vulnerability...\\n"
    print "[+] Find the legitimate dylib: find / -name <dylibname>, and note the path\\n"
    print "[+] Run the CreateHijacker module in /persistence/osx/. Set the DylibPath to the path of the legitimate dylib.\\n"
run()
""" % (scanPath, LoadedProcesses)
        return script