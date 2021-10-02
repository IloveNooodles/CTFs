from pwn import *

elf = ELF("./chall")
elf.process()

def check(x, y):

  a = y*10 & 255
  b = (a+1337)*16
  return b*a + (a^b^y) * y^x

arr = []
for y in range(1, 0x100):
  for i in range(0, 1 << 31):
    if check(i, y) == 0:
      arr.append(i)

print(arr)
