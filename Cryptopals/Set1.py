import binascii
import base64

# Challenge 1
'''
a = '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d'
a_decoded = binascii.unhexlify(a)
ab64 = base64.b64encode(a_decoded)
print(ab64)
'''

#Challenge 2
'''
def fxor(a, b):
  a_decoded = int(a, 16)
  b_decoded = int(b, 16)
  c = a_decoded ^ b_decoded
  c_encoded = hex(c)
  return c_encoded[2:]

print(fxor('1c0111001f010100061a024b53535009181c', '686974207468652062756c6c277320657965'))
'''

#Challenge 3

list = []
a = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
print(binascii.unhexlify(a))
# for i in range(26):
#   b = a ^ chr(i)
#   print(b)

