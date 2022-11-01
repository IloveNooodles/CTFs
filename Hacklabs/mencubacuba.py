import random

# flag = 'REDACTED'
# result = []
# hehe = random.randint(100000, 1000000)
# for i in range(len(flag)):
# 	result.append(ord(flag[i]) ^ hehe)
# print(result)


res = [
    681557,
    681564,
    681566,
    681558,
    681553,
    681564,
    681567,
    681550,
    681574,
    681567,
    681583,
    681576,
    681577,
    681518,
    681538,
    681563,
    681586,
    681551,
    681598,
    681518,
    681538,
    681579,
    681518,
    681551,
    681572,
    681538,
    681557,
    681518,
    681513,
    681585,
    681577,
    681589,
    681540,
    681568,
]

for i in range(100000, 1000001):
    if chr(res[0] ^ i) == "H":
        print(i)

for i in range(len(res)):
    print(chr(res[i] ^ 681501), end="")
