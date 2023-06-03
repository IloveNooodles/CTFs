from binascii import crc32

from Crypto.Util.number import long_to_bytes as l2b
from Crypto.Util.Padding import pad

f = open("./Participant/chall.png", "rb")
data = f.read()
f.close()

IHDR = data.find(b"IHDR")
PHYS = data.find(b"pHYs")

length = PHYS - IHDR

n_width = 720
n_heigth = 740

new_crc = (
    b"IHDR"
    + l2b(n_width).rjust(4, b"\x00")
    + l2b(n_heigth).rjust(4, b"\x00")
    + b"\x08\x06\x00\x00\x00"
)

calculated_crc = crc32(new_crc)
new_crc += l2b(calculated_crc).rjust(4, b"\x00")

new_data = data[:IHDR]
new_data += new_crc
new_data += data[PHYS - 4 :]

f = open("tmp.png", "wb")
f.write(new_data)
f.close()
