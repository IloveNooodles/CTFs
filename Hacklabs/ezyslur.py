import random

random.seed(0)
# flag = "REDACTED"
# result = ""
# for i in range(len(flag)):
#     a = random.randint(32, 127)
#     result += hex(ord(flag[i]) ^ random.randint(32, 127))

#     temp = res
# print(result)

res = "0x190x140x660xa0x2d0x1f0x110x150x260x3e0x5b0x560x100x5d0x210x6e0x740x200x120x3b0x90x5c0x5f0x370x400x180x760x250x7e0x320x230x730x3e0x660x250x1e0x1d0x5f0x390x150x6b0x3a0x3c"
# for i in range(0, len(res), 4):
#     hex_ = res[i : i + 4]
#     print(hex_, end=" ")
a = res.split("0x")[1:]
for i in a:
    c = "0x" + i
    b = int(c, 16)
    b ^= random.randint(32, 127)
    print(chr(b), end="")
    # print(b, end="")


# # a = hex(ord(flag[i])) ^ random.radint(32,127)
# # a ^= random.radint(32,127)
# # a = int(a, 16)
# # a = chr(a)
