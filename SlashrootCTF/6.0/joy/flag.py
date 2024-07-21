from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from binascii import unhexlify

import os

block_size = 128

key = b"\xf5\xbc\x05\x9d\x85\x1d|/C<\xfb\x90\x16\xe4Zo"

msg = b"95fc28829a9f02ccdfad3af5a7ddb202814d6421b716493f3f12d55e88fc1f6a7d81b72615c4e715db5ba7e3d512d8d371eb0eef666488ee83626c5d853e1a5c1468a51b5641b54a62515110729aa8401468a51b5641b54a62515110729aa8401468a51b5641b54a62515110729aa8401468a51b5641b54a62515110729aa840"

cipher = AES.new(key, AES.MODE_ECB)


def decrypt(msg):
    return unpad(cipher.decrypt(msg), block_size)


print(decrypt(unhexlify(msg)).decode("latin1"))
