import numpy as np

flag = 'slashroot7{ul412_1s_k3y}'
print(len(flag))

np.random.seed(12345)
arr = np.array([ord(c) for c in flag])
other = np.random.randint(1, 5, (len(flag)))
arr = np.multiply(arr, other)

b = [x for x in arr]
# print(b)
lmao = [ord(x) for x in ''.join(['slashroot_ctf_'*5])]
c = [b[i] ^ lmao[i] for i, j in enumerate(b)]

print(c)
idx = [9 if x >= 256 else 8 for x in c]
print(idx)
a = ''.join(bin(x)[2:].zfill(8) for x in c)
print(len(a))
