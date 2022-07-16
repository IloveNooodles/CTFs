from Crypto.Util.number import *
import sys

message = b'gare'

def enkrip(m, baits):
	p = getPrime(1024)
	q = getPrime(1024)
	n = p*q
	return( n , pow(bytes_to_long(m[:baits]),baits,n))

#ngereturn n nya sama m^e mod n

n, c = enkrip(message, 1)
print(n, c)