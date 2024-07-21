#!/usr/bin/env python3
from Crypto.Util.number import *

def gen_key(e):
    while True:
        p = getPrime(512)
        q = getPrime(512)
        phi = (p-1) * (q-1)
        if GCD(e, phi) == 1:
            return e, p, q

def random_stuff(m, l):
    range_ = l - bytes_to_long(m).bit_length()
    padding = long_to_bytes(getRandomNBitInteger(range_))
    if len(padding) > 0xff:
        raise ValueError("Padding length exceed 0xff")
    result = bytes_to_long(chr(len(padding)).encode("latin1") + padding + m)
    return long_to_bytes(result << 2)

if __name__ == "__main__":
    FLAG = "GARE"
    # FLAG = open("flag.txt", "rb").read()
    part1 = b"".join([chr(FLAG[i]).encode() for i in range(0, len(FLAG), 2)])
    part2 = b"".join([chr(FLAG[i]).encode() for i in range(1, len(FLAG), 2)])

    while True:
        e1, p1, q1 = gen_key(3)
        n1 = p1 * q1
        f1 = bytes_to_long(random_stuff(part1, 335))
        if pow(f1, e1) > n1:
            break
    
    e2, p2, q2 = gen_key(65537)
    n2 = p2 * q2
    f2 = bytes_to_long(part2)
    
    ct1 = pow(f1, e1, n1)
    ct2 = pow(f2, e2, n2)
    r = pow(5*p2 + 4*q2, e1, n2)
    s = pow(9*p2 + 5*q2, e2, n2)
    
    print(f"n1 = {n1}")
    print(f"n2 = {n2}")
    print(f"ct1 = {ct1}")
    print(f"ct2 = {ct2}")
    print(f"r = {r}")
    print(f"s = {s}")