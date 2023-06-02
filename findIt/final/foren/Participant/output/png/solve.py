import zlib

f = open("flag.png", "rb")
data = f.read()
f.close()
IDAT = data[0x94:0x10840]

uncompressed = IDAT[12:]
print(uncompressed)
