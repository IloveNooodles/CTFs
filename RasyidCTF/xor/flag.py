#!/usr/bin/env python3

from binascii import *
from itertools import cycle

flag = "051807153d347135197d3218273b72347621243a"
flag = unhexlify(flag)


key = "FLAG"
key = key.encode()

def bxor(b1, b2):
	result = b""
	for b1, b2 in zip(b1, cycle(b2)): 
		result += bytes([b1^b2])
	return result

ans = bxor(flag,key)
print(ans.decode())
