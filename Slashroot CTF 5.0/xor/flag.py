###!/usr/bin/python 3

from binascii import *
from itertools import cycle

flag = "63a0326fb5485ef41f8f4bba606ea46542aa06ca5cff0c64ed484c"
flag = unhexlify(flag);

key = b'\x16F\x14'


print(flag)

def bxor(b1, b2):
  result = b""
  for b1, b2 in zip(b1, cycle(b2)):
    result += bytes([b1^b2])
  return result

print(bxor(flag, key))

