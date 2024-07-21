#!/usr/bin/python

from pwn import *

# Pass the nc hostname port
CONN = "nc localhost 1337".split(" ")
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


def start(argv=[], *a, **kw):
    if args.GDB:
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:
        return remote(HOST, PORT, *a, **kw)
    else:
        return process([exe] + argv, *a, **kw)


# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

def exploit(io):
    offset = 64

    # Build the payload
    payload = flat({offset: []})

    # Send the payload
    sla(b"> ", payload)
    ru(b"Thank you!")

    # Got Shell?
    io.interactive()

# ===========================================================
#                           SETUP
# ===========================================================


if __name__ == "__main__":

    # Specify GDB script here (breakpoints etc)
    gdbscript = """
    c
    """.format(
        **locals()
    )

    # Binary filename
    exe = "./vuln"

    # This will automatically get context arch, bits, os etc
    elf = context.binary = ELF(exe, checksec=False)
    rop = ROP(elf)

    # Change logging level to help with debugging (error/warning/info/debug)
    context.terminal = "tmux splitw -h".split(" ")
    context.log_level = "debug"

    # Lib-C library, can use pwninit/patchelf to patch binary
    libc = elf.libc
    ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

    if args.REMOTE:
        pass
        # libc = ELF("libc.so.6", checksec=False)
        # ld = ELF("ld-linux-x86-64.so.2", checksec=False)

    io = start()

    exploit(io)
