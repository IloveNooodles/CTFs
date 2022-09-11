# Import the pwntools library
# You can install this via pip install pwntools
# nc 103.41.205.26 10075
from pwn import *

# To process local files
# r = process('./filename')

# To connect to a remote server via nc
r = remote('103.41.205.26', 10075)

r.recvline()
while(True):
  try:    
    data = r.recvuntil(b"=").decode()
    data = data.split("=")
    print(data[0])
    ans = eval(data[0])
    r.sendline(str(ans).encode("latin-1"))
  except:
    r.interactive()

