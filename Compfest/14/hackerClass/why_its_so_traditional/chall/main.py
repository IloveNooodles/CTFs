import math
from Crypto.Util.number import bytes_to_long


def cc_encrypt(plain: str):
    cipher = ""
    for i in range(len(plain)):
        assert ord(plain[i]) < 128
        if i == len(plain) - 1:
            cipher += plain[i]
        else:
            cipher += chr((ord(plain[i]) + ord(plain[i + 1]) - 2*32) % 94 + 32)
    return cipher

def bc_encrypt(plain: str):
    file = open("lorem.txt", "r")
    tmp = file.read()
    file.close()
    off = 0

    cipher = ""
    for i in range(len(plain)):
        chr = str(bin(ord(plain[i]) - 32))[2:].zfill(7)
        assert len(chr) == 7
        for j in chr:
            while (not tmp[off].isalpha()):
                off += 1
            if j == "1":
                cipher += tmp[off].capitalize()
            else:
                cipher += tmp[off].lower()
            off += 1
    return cipher

def ct_encrypt(plain: str):
    file = open("lorem.txt", "r")
    key = file.read()[0:5].lower()
    file.close()

    cipher = ""
  
    lst = list(plain)
    key_srt = list(key)
    key_srt.sort()

    col = len(key)
    row = math.ceil(len(plain)/col)
    lst = []
 
    for i in range(row):
        tmp = []
        for j in range(col):
            if ((i*col) + j < len(plain)):
                tmp.append(plain[(i*col) + j])
            else:
                tmp.append(" ")
        lst.append(tmp)

    for i in range(col):
        tmp = key.index(key_srt[i])
        for j in range(row):
            cipher += lst[j][tmp]
        
    return cipher

def vc_encrypt(plain: str):
    file = open("lorem.txt", "r")
    key = file.read()[0:5].lower()
    file.close()

    cipher = ""
    for i in range(len(plain)):
        assert ord(plain[i]) < 128
        cipher += chr((ord(plain[i]) + ord(key[i % len(key)]) - 64) % 94 + 32)

    return cipher


def encrypt(plain: str):
    cipher = ""
    cipher += cc_encrypt(plain[0:20])
    cipher += bc_encrypt(plain[20:40])
    cipher += ct_encrypt(plain[40:60])
    cipher += vc_encrypt(plain[60:])  
    return bytes_to_long(bytes(cipher, encoding='utf-8'))

def main():
    file = open("flag.txt", "r")
    plain = file.read()
    file.close()
    tmp = encrypt(plain)
    file = open("cipher.txt", "w")
    file.write(str(tmp))
    file.close()

if __name__ == "__main__":
    main()

