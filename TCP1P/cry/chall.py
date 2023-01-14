#!/usr/bin/python
import binascii

FLAG = 'REDACTED'
KEY = "REDACTED" # DELETED

def encrypt(plaintext):
    enc = []
    for s in plaintext:
        enc.append(ord(s) ^ KEY)
    return bytes(enc)

# with open('encrypted.txt', 'wb') as f:
#     f.write(b'FLAG: ' + binascii.hexlify(encrypt(FLAG)))

def find_key(ciphertext: bytes):
  for i in range(0xff):
      if chr(ciphertext[0] ^ i) == 'T' and chr(ciphertext[1] ^ i) == 'C':
          print(i)

def decrypt(ciphertext: bytes):
  pt = ""
  for i in range(len(ciphertext)):
    pt += chr(ciphertext[i] ^ 160)
  
  print(pt)
  

with open("encrypted.txt", "rb") as f:
    text = f.read().decode()
    text = text.split(" ")[1]
    ct = binascii.unhexlify(text)
    decrypt(ct)
    
    