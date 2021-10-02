from random import *
from binascii import *
from Crypto.Util.number import *
from pwn import *

# class LCG:
#     def __init__(self, seed):
#         self.mod = 65537
#         self.mult = 42152
#         self.inc = 21735
#         self.state = seed

#     def next(self):
#         self.state = (self.state * self.mult + self.inc) % self.mod
#         return self.state

# def crack_unknown_increment(states, modulus, multiplier, i):
#     increment = (states[i+1] - states[i]*multiplier) % modulus
#     return modulus, multiplier, increment

# def crack_unknown_multiplier(states, modulus, i):
#     multiplier = (states[i+2] - states[i+1]) * inverse(states[i+1] - states[i], modulus) % modulus
#     return crack_unknown_increment(states, modulus, multiplier)

# flag_content = open("flag.txt").read().strip()
# nc 103.145.226.170 1011
p = remote("103.145.226.170", "1011")
p.recvuntil(b"\n")


# flag = [10314, 29195, 49062, 12137, 56467, 33489, 43269, 36195, 47943, 30491, 47969, 64649, 42004, 35544, 63841, 32372, 28312, 5684, 39146, 24839, 64360, 20536, 58580, 46983, 19235, 53131, 58543, 3045, 29740, 26168, 46101, 48019, 25362, 56880, 26737, 55065, 50835, 43477, 7338, 20989, 9584, 10334, 18850, 25254, 24303, 19982, 32483, 9655, 49063]

# for i in range(2, 1 << 16):
#   temp = [chr(i^x) for x in flag]
#   text = "".join(temp)
#   print(text)




# seed = randint(2, (1<<16)-2)
# r = LCG(seed)
# mod = r.mod
# ans = []
# arrR = [r.state]
# arrR.append(r.next())
# arrR.append(r.next())

# a, b, c = crack_unknown_multiplier(arrR, mod)
# print(a, b, c)


# # while True:
# #     print("Menu:")
# #     print("[1] Guess flag")
# #     print("[2] Encrypt message")
# #     print("[3] Exit")
# #     inp = input("Input: ")

# #     if inp == "1":
# #         guess = input("Your guess: ")
# #         if guess == flag_content:
# #             print("NOICE!!!")
# #             print(f"Here is your flag: Slashroot5{{{flag_content}}}")
# #             exit()
# #         else:
# #             print("Nope....")
# #     elif inp == "2":
# #         msg = input("Your message: ")
# #         plain = flag_content + "||" + msg
# #         res = [r.next() ^ ord(x) for x in plain]

# #         print(f"Here is your encrypted message: {res}")
# #     elif inp == "3":
# #         exit()
# #     else:
# #         print("Unknown input...")
# #     print()

# flag = [23178, 56865, 22460, 33544, 41250, 15662, 16669, 10354, 47489, 39007, 38417, 31974, 52487, 28943, 52738, 59296, 34168, 3404, 11840, 30455, 18099, 27331, 24835, 22079, 31694, 50735, 25318, 15505, 54139, 43979, 2079, 31262, 53096, 12188, 257, 62990, 8291, 34702, 24248, 32509, 26174, 42064, 5263, 22202, 18838, 1981, 32315, 8178, 8435]
# for i in range(2, 2**16):
#   a = LCG(i)
#   res = [chr(a.next() ^ x) for x in flag]
#   text = "".join(res)
#   if "|" in text:
#     try:
#       text = text.encode('utf-16')
#       print(text)
#     except:
#       continue