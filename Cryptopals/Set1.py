from binascii import hexlify, unhexlify
from base64 import b64decode, b64encode

def hextobase64(a):
  return b64encode(unhexlify(a))

def bxor(a, b):
  return bytes([a^b for (a, b) in zip(a, b)])

def score(a):
  sums = sum([x in goodcharacter for x in a])
  return sums / len(a)

def ratio(a):
  r = score(a)
  return r > 0.7

def singlebytesxor(a):
  candidates = []
  for i in range(1, (1 << 8)):
    char = bytes([i])
    key = char*len(a)
    decode = bxor(a, key)
    r = ratio(decode)
    if(r):
      candidates.append(unhexlify(hexlify(decode)))
  return candidates


goodcharacter = [i for i in range(ord('a'),  ord('z') + 1)] + [ord(' ')]

# Challenge 1

'''
a = b'49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
print(hextobase64(a))
'''

#Challenge 2

'''
a = unhexlify('1c0111001f010100061a024b53535009181c')
b = unhexlify('686974207468652062756c6c277320657965')
print(hexlify(bxor(a, b)))
'''

#Challenge 3

'''
cipher = unhexlify('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
print(singlebytesxor(cipher))
'''

