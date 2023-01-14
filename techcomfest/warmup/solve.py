#!/usr/bin/env python3

import string

from pwn import *

exe = ELF("./chall", checksec=False)

context.binary = exe

index = [
    1,
    14,
    18,
    34,
    39,
    42,
    48,
    51,
    59,
    61,
    62,
    77,
    84,
    89,
    94,
    105,
    107,
    116,
    120,
    124,
    140,
    142,
    150,
    151,
    152,
    158,
    173,
    181,
    189,
    199,
    201,
    207,
    210,
    214,
    215,
    226,
    228,
    229,
]


def conn():
    if args.LOCAL:
        r = process([exe.path])
        if args.DEBUG:
            gdb.attach(r)
    else:
        r = remote("103.49.238.77", 64012)

    return r


def main():
    r = conn()

    num = r.clean()
    list_num = num.decode().split(" ")[:-1]
    for i in index:
        print(chr(int(list_num[i])), end="")


if __name__ == "__main__":
    main()
