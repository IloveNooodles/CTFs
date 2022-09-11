import sys
import base64
from Crypto.Util.number import *
from pwn import *
import requests
import json

# HOST = "socket.cryptohack.org" 
# PORT = 11112

# p = remote(HOST, PORT)

# data = {"buy" : "flag"}

# p.recvuntil("ok.")
# p.send(json.dumps(data))
# p.interactive()

# def bxor(b1, b2):
#   ans = b''
#   for (a, b) in zip(b1, b2):
#     ans += bytes([a^b])
#   return ans

# #1
# # import this

# if sys.version_info.major == 2:
#     print("You are running Python 2, which is no longer supported. Please update to Python 3.")

# ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]

# print("Here is your flag:")
# print("".join(chr(o ^ 0x32) for o in ords))

#2

# arr = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]
# for item in arr:
#   print(chr(item), end='')

#3

# s = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"
# print(bytes.fromhex(s))

#4
# s = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"
# s = bytes.fromhex(s)
# s = base64.b64encode(s)
# print(s)

#5
# l = 11515195063862318899931685488813747395775516287289682636499965282714637259206269
# l = long_to_bytes(l)
# print(l)

#6
# s = "label"
# for char in s:
#   print(chr(ord(char)^13))

#7
# key1 = "a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313"
# key1 = bytes.fromhex(key1)
# key12 = "37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e"
# key12 = bytes.fromhex(key12)
# key23 = "c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1"
# key23 = bytes.fromhex(key23)
# key123flag = "04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf"
# key123flag = bytes.fromhex(key123flag)

# key2 = xor(key1, key12)
# key3 = xor(key2, key23)
# flag = xor(key1, key2, key3, key123flag)
# print(flag)

#8
# s = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"
# s = bytes.fromhex(s)
# for i in range(1, 255):
#   if b"crypto" in xor(s, i):
#     print(xor(s, i))
  

#9
# s = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
# s = bytes.fromhex(s)
# key = b'myXORkey'
# print(xor(s, key))