#!/usr/bin/env python3
from Crypto.Util.number import getStrongPrime, long_to_bytes
from random import getrandbits
from hashlib import sha256
from secret import FLAG

p = getStrongPrime(1024)
q = getStrongPrime(1024)
N = p * q
e = 0x17

def rand():
    randbits = [getrandbits(32) << 32 * i for i in reversed(range(0, 6))]
    return randbits[0] | randbits[1] | randbits[2] | randbits[3] | randbits[4] | randbits[5]

def get_random_pad():
    return int(sha256(long_to_bytes(rand())).hexdigest(), 16)

def get_flag():
    return pow(FLAG + get_random_pad(), e, N)

def show_menu():
    print(f"{'=' * 20} Random Store Automated {'=' * 20} \
        \nWelcome to my Random Store! What can I do for ya? \
        \n[1] Get a Random 192-bit Number \
        \n[2] Get Encrypted Flag \
        \n[3] Exit \
        \n{'=' * 64}")

def main():
    while(1):
        show_menu()
        inp = input("> ")
        if(inp == '1'):
            print(f"Your random number is: {hex(rand())}\n")
        elif(inp == '2'):
            print(f"e: {hex(e)}")
            print(f"N: {hex(N)}")
            print(f"Your encrypted flag is: {hex(get_flag())}\n")
        elif(inp == '3'):
            print("Pleased to serve you, good luck with the rest of your adventure!\n")
            exit()
        else:
            print("Sorry, we don't have any of that here.\n")

if(__name__ == "__main__"):
    main()
