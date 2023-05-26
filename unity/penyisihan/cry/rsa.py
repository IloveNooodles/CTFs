import sympy
from Crypto.Util.number import *

e = 0x10001
n = 125552589999191
c = 101003677696797
print(sympy.totient(n))
tot = int(sympy.totient(n))
d = pow(e, -1, tot)
test = 2
assert pow(test, e * d, n) == test
print(pow(c, d, n))
print(long_to_bytes(pow(c, d, n)))
