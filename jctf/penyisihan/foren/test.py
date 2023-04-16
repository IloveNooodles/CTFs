from pwn import *

f = open("spartan_disk", "rb")
data = f.read()

length_data = len(data)
key = b"godofwargodofwar"
a = xor(key, data)

f2 = open("a", "wb")
f2.write(a)
