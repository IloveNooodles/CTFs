from pwn import *

conn = "nc saturn.picoctf.net 57187"
host = conn.split(" ")[1]
port = conn.split(" ")[2]

p = remote(host, port)

p.sendline(b"040129e")
f = p.recvall()
flag = f.decode().split("picoCTF")
print("picoCTF" + flag[1])
