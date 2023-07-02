#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("malloc_testbed")
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

# Select the "malloc" option; send size.
# Return chunk index.
def malloc(size):
    global index
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}".encode())
    io.recvuntil(b"> ")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

# Select the "free address" option; send address.
def free_address(address):
    io.send(b"3")
    io.sendafter(b"address: ", f"{address}".encode())
    io.recvuntil(b"> ")

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send(b"4")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

# Select the "read" option; send index.
# Return data from read operation.
def read(index):
    io.send(b"5")
    io.sendafter(b"index: ", f"{index}".encode())
    r = io.recvuntil(b"\n1) malloc", drop=True)
    io.recvuntil(b"> ")
    return r

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts

# This binary leaks the heap start address.
io.recvuntil(b"heap @ ")
heap = int(io.recvline(), 16)

# This binary leaks the address of its m_array.
io.recvuntil(b"m_array @ ")
m_array = int(io.recvline(), 16)
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# =-=-=- EXAMPLE -=-=-=

# Log some useful addresses.
info(f"libc is at 0x{libc.address:02x}")
info(f"heap is at 0x{heap:02x}")
info(f"m_array is at 0x{m_array:02x}")

# Request 2 chunks.
chunk_A = malloc(0x88)
chunk_B = malloc(0x18)

# Free "chunk_A".
free(chunk_A)

# Edit "chunk_B".
edit(chunk_B, b"Y"*8)

# Read data from the "chunk_B".
info(f"reading chunk_B: {read(chunk_B)[:8]}")

# =============================================================================

io.interactive()
