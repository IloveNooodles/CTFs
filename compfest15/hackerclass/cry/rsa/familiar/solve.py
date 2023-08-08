#!/usr/bin/python

from pwn import *
from Cryptodome.Util.number import long_to_bytes, bytes_to_long
import binascii

def sl(x): io.sendline(x)
def sla(x, y): io.sendlineafter(x, y)
def se(x): io.send(x)
def sa(x, y): io.sendafter(x, y)
def ru(x, drop=False): return io.recvuntil(x, drop=drop)
def rl(): return io.recvline()
def cl(): io.clean()
def un64(x): return u64(x.ljust(8, b'\x00'))
def leak(name, addr): info(f"{name} @ {hex(addr)}")

io = remote("34.101.174.85", 10000)


def encrypt(msg=b"00"):
  sla(b"> ", b"2")
  sla(b"=", msg)
  ru(b": ")
  return rl()
  

def decrypt(msg: bytes):
  return binascii.unhexlify(msg.decode().strip())

BLOCK_SIZE = 16
REALFLAG = "COMPFEST15{afdd2f3f203a7ee5055bbadb15302b9c1b81b78a747901fd3232dbd9ff479495}"
flag = binascii.hexlify(REALFLAG.encode())
while True:
  payload = b"0" * (254 - len(flag))
  cur = encrypt(payload)

  for i in range(30, 125):
    c = binascii.hexlify(int.to_bytes(i))
    tosend = payload + flag + c
    txt = encrypt(tosend)
    # print("Cur: ", cur[:64])
    # print("Try: ", txt[:64])
    if cur[:256] == txt[:256]:
      flag += c
      REALFLAG += chr(i)
      break

  print("RealFlag: ", REALFLAG)
        
io.interactive()


