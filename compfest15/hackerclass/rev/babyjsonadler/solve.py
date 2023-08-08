#!/usr/bin/python
from Cryptodome.Util.number import bytes_to_long as b2l

f = open("./enc2.txt", "rb")
data = f.read()
# print(data)
f.close()

arr = []
for val in data:
  arr.append(val)

print(len(arr))

holder2 = []
for idx, val in enumerate(arr[199:]):
  if idx == 0:
    holder2.append(val)
  else:
    holder2.append((idx + arr[idx - 1]) % 131072)

arr[199:] = holder2
holder1 = []
for idx, val in enumerate(data):
  if idx == 0:
    holder1.append(val - 1)
  else:
    holder1.append((holder1[0] + holder1[idx - 1]) % 33554432)

print(holder1, len(holder1))

for c in holder1:
  print(chr(c), end="")