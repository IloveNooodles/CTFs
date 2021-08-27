# -*- coding: utf-8 -*-
import random
random.seed("wadidaw")

data = open('out.txt').read()
flag = "REDACTED"
out = ""


for i in range(len(data)):
  a = random.randint(0x00, 0xFF)
  b = random.randint(0x00, 0xFF)
  for j in range(0xFF):
    if chr(((j ^ a)+b)% 0xFF) == data[i]:
      print(chr(j))

# for c in flag:
# 	out += chr( ((ord(c) ^ random.randint(0x00, 0xFF)) + random.randint(0x00, 0xFF) ) % 0xFF)

