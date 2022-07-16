#!/usr/bin/env python3
from Crypto.Util.number import *
from secret import flag
import sys

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, datas):
        self.stream.writelines(datas)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def enkrip(m, baits):
	p = getPrime(1024)
	q = getPrime(1024)
	n = p*q
	return( n , pow(bytes_to_long(m[:baits]),baits,n))

long2str(n)

for chances in range(7):
	baits = int(input("[?] How many bytes? "))
	assert(baits > 0)
	n, c = enkrip(flag, baits)
	print("[+] Your public-K : ", hex(n)[2:])	
	print("[+] Your cipher : ", hex(c)[2:])

print("[!] Times Out !")
exit()