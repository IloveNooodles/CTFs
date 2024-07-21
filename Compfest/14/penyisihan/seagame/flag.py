from pwn import *
# nc 103.185.38.43 13001
# while(1):

# nc 103.185.38.43 13000

def send_payload(p, number):
  p.recvuntil(b"one : ")
  text = f"{number}"
  text = bytes(text)
  print(text)

p = remote("103.185.38.43", 13000)
p.recvuntil(b"one : ")
p.sendline(b"2")
send_payload(p, 2)
p.interactive()