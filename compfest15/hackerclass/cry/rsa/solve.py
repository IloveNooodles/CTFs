#!/usr/bin/python
import gmpy2
from Cryptodome.Util.number import *
from sympy import Pow, nextprime

from pwn import *

CONN = "nc 34.101.174.85 10004".split(" ")
HOST = CONN[1]
PORT = CONN[2]

# ===========================================================
#                    WRAPPER FUNCTION
# ===========================================================

def sl(x): io.sendline(x)
def sla(x, y): io.sendlineafter(x, y)
def se(x): io.send(x)
def sa(x, y): io.sendafter(x, y)
def ru(x, drop=False): return io.recvuntil(x, drop=drop)
def rl(): return io.recvline()
def cl(): io.clean()
def un64(x): return u64(x.ljust(8, b'\x00'))
def leak(name, addr): info(f"{name} @ {hex(addr)}")

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    return remote(HOST, PORT, *a, **kw)


io = start()
def get_input():
  rl()
  mode = rl().decode().strip().split("= ")[1]
  n = int(rl().decode().strip().split("= ")[1])
  e = int(rl().decode().strip().split("= ")[1])
  c = int(rl().decode().strip().split("= ")[1])
  
  return mode, n, e, c

def rsa(mode, n, e, c):
  if mode == 'A':
    totN = n - 1
    d = inverse(e, totN)
    m = pow(c, d, n)
    return m
  elif mode == 'B':
    m = int(gmpy2.iroot(c, 3)[0])
    return m
  elif mode == 'C':
    nearN = int(gmpy2.iroot(n, 2)[0])
    p = nearN
    q = None
    while True:
      p = nextprime(p)
      q = n // p
      print("[+] Trying p: ", p)
    
      if p * q == n:
        break
      
      if p > n:
        print("[-] Failed")
        break
    
    totN = (p - 1)*(q-1)
    d = inverse(e, totN)
    m = pow(c, d, n)
    return m
      
  

def solve():
  for i in range(20):
    mode, n, e, c = get_input()
    print(i)
    m = rsa(mode, n, e, c)
    sla(b": ", str(m).encode())
  
  io.interactive()
if __name__ == "__main__":
  solve()