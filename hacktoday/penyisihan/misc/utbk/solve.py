#!/usr/bin/python
import json

from pwn import *

CONN = "nc 103.181.183.216 19003".split(" ")
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

# ===========================================================
#                           SETUP
# ===========================================================

# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
  return remote(HOST, PORT, *a, **kw)

f = open("./list.json", "r")
wordlist = json.load(f)
f.close()


io = start()


# =========== Get available Wordlist
def getwordlist():
  io = start()
  
  ru(b"\n\n")
  rl()
  rl()

  def get_problem_and_ans():
    problem = rl().decode().strip()
    sl(b"a")
    ru(b"adalah ")
    ans = rl().decode().strip()
    rl()
    rl()
    
    return problem, ans

  for i in range(3):
    problem, ans = get_problem_and_ans()
    wordlist[problem] = ans.strip()

  f = open("list.json", "w")
  f.write(json.dumps(wordlist))
  f.close()
  
  io.clean()
  io.close()
  sleep(2)

# for i in range(1000):
#   try:
#     getwordlist()
#   except:
#     pass

# ==== Receive input
ru(b"\n\n")
rl()
rl()

def answer(i):
  problem = rl().decode().strip()
  print("Solving question ", i, problem)
  
  if problem in wordlist:
    ans = wordlist[problem]
    sl(ans.encode())
    rl()
    rl()
    rl()
  else:
    sl(b"a")
    ru(b"adalah ")
    ans = rl().decode().strip()
    rl()
    rl()
  
  
for i in range(99):
  answer(i)
  sleep(0.1)

io.interactive()