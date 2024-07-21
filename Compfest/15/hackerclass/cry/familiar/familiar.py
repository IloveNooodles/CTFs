#!/usr/bin/python

from ast import Assert
import sys
import os
import binascii
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
# from secret import FLAG
from time import sleep

IV = os.urandom(AES.block_size)
KEY = os.urandom(AES.block_size)

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

FLAG = b"COMPFEST2023{INI_CONTOH_FAKE_FLAG_PANJANG_BGT_LOH_MIN_RIL}"

def get_flag():
    print("Sorry, the get_flag function is currently broken. Please try something else.")

def encrypt(msg: str = None):
    if msg == None:
        msg = input("message (in hex) = ")
    assert len(msg) % 2 == 0, f"Invalid Odd-length string of {msg} has been inputted."
    print(msg)
    try:
        msg = binascii.unhexlify(msg) + FLAG
    except:
        raise AssertionError(f"{msg} is not a valid hex representation.")
    enc = AES.new(KEY, AES.MODE_ECB)
    print(msg, len(msg))
    cipher = enc.encrypt(pad(msg, 16))
    # print("ciphertext (in hex): " + binascii.hexlify(cipher).decode())
    return binascii.hexlify(cipher).decode()

#DEPRECATED
def decrypt():
    print("Sorry, the decrypt function is currently broken. Please try something else.")

def menu():
    print("1. Get encrypted flag")
    print("2. Encrypt a message")
    print("3. Decrypt a message")
    print("4. Exit")

def main():
    try:
        while True:
            menu()
            choice = input("> " )
            if choice == "1":
                get_flag()
            elif (choice == "2"):
                ct = encrypt()
                flag = b""
                while True:
                  payload = b"0" * (62 - len(flag))
                  cur = encrypt(payload)

                  for i in range(1, 0xff):
                      c = binascii.hexlify(int.to_bytes(i))
                      tosend = payload + flag + c
                      txt = encrypt(tosend)
                      print(tosend)
                      print(len(tosend))
                      print("Cur: ", cur[:64+2])
                      print("Try: ", txt[:64+2])
                      if cur[:64] == txt[:64]:
                        flag += c
                        print("KETEMU", flag)
                        sleep(3)
                        break
            elif (choice == "3"):
                decrypt()
            elif (choice == "4"):
                print("ending session.")
                break
            else:
                print("invalid input.")
    except Exception as e:
        print(repr(e))

if __name__ == "__main__":
    main()


# from pwn import *

# def sl(x): io.sendline(x)
# def sla(x, y): io.sendlineafter(x, y)
# def se(x): io.send(x)
# def sa(x, y): io.sendafter(x, y)
# def ru(x, drop=False): return io.recvuntil(x, drop=drop)
# def rl(): return io.recvline()
# def cl(): io.clean()
# def un64(x): return u64(x.ljust(8, b'\x00'))
# def leak(name, addr): info(f"{name} @ {hex(addr)}")

# # io = remote("34.101.174.85", 10000)


# def encrypt(msg=b"00"):
#   sla(b"> ", b"2")
#   sla(b"=", msg)
#   ru(b": ")
#   return rl()[:96+2]
  

# def decrypt(msg: bytes):
#   return binascii.unhexlify(msg.decode().strip())


# BLOCK_SIZE = 16
# flag = b""
# while True:
#   payload = b"00" * (55 - len(flag))
#   cur = encrypt(payload)

#   for i in range(1, 0xff):
#       c = binascii.hexlify(int.to_bytes(i))
#       tosend = payload + flag + c
#       txt = encrypt(tosend)
#       print(tosend)
#       print("Cur: ", cur)
#       print("Try: ", txt)
#       if cur == txt:
#         flag += c
#         print("KETEMU", flag)
#         break

#   print("Flag: ", flag)
        
# io.interactive()


