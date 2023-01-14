from Crypto.Util.number import long_to_bytes

with open("flag.txt", "r") as f:
    txt = f.read()
    txt = txt.split("-")
    for i in txt:
        print((long_to_bytes(int(i, 16)).decode())[::-1], end="")
