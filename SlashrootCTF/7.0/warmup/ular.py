import numpy as np

np.random.seed(12345)

f = open("./output.txt")
data = f.read()
f.close()

# Try to get 9 and 8
idx = [
  9, 8, 8, 8, 8, 8, 9, 9, 8, 8, 
  8, 8, 9, 8, 8, 8, 8, 8, 9, 9, 
  8, 8, 8, 9]

flag_char = []
data_offseet = 0
for i in range(len(idx)):
  numstr = data[data_offseet:data_offseet+idx[i]]
  num = int(numstr, 2)
  flag_char.append(num)
  data_offseet += idx[i]

lmao = [ord(x) for x in ''.join(['slashroot_ctf_'*5])]

c = [flag_char[i]^lmao[i] for i,j in enumerate(flag_char)]
other = np.random.randint(1,5,(len(c)))
flag = np.floor_divide(c, other)

flag = ''.join([chr(x) for x in flag])
print(flag)
  
