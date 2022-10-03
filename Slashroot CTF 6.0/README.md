# Pwn

## Pink_venom

use `nl` as `cat` substitute.  
Flag: `slashroot6{Wh0_mad3_th1s_Sh1tty_Bs4h_j4il????}`

# rev

## solo_lord

decompile ghidra, input 63 and 5. Stonks.  
Flag: `slashroot6{kuk1r4_by_0n3_t3rny4t4_b4w4_k4w4n}`

## YNTKTS

```py
from Crypto.Util.number import *
ct = b'4v)npmD|+o(it=3v(iD`)|3b'
def decrypt(ct):
    flag = b''
    for i in range(len(ct)):
        c = ct[i]
        if (i%2==0):
            c -= 5
            c = c^2
        c^=0x1b
        c-=0x06
        flag =long_to_bytes(c) + flag
    return flag

print(decrypt(ct))

```

Flag: `slashroot6{s1a7u l4g1 pl4n9a plo7g0}`

## DoraCTF

1. Fix Header PNG
2. Decompile using jadx-gui and apktool
3. Get image from web `https://indrayyana.github.io/`
4. use steghide with this pass `sw1p3r_n0_sw1p1ng`
5. stonks

Flag: `slashroot6{3v3rything_1s_4_w1dg3t_1n_flutt3r}`

# Joy

## app-debug

1. use apkdecompiler
2. run script
3. stonks

```py
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
```

Flag: `slashroot6{tr0ll_aLwayS_th3_fIrsT_uAO00agh_s0rry}`

# OSINT

## Hatake Bapak

Cari username di tiktok make rev image
Flag: `slashroot6{@ketut.lelutcellelut}`

## Phone number

1. Cari sponsoring registar number di `https://iwhois.webnic.cc/jsp/whois_captcha.jsp`

Flag: `slashroot6{0274882257}`

# Crypto

## rcRcRCrC

```py
from pwn import * # pip install pwntools
import json
import codecs
from Crypto.Util.number import long_to_bytes

ip = "103.152.242.37"
#sock = int

sock = 10103

r = remote(ip, sock)

r.recvuntil(b": ")
r.sendline(b'1')
r.recvuntil(b": ")
ct = r.recvline()[:-1]
print(ct)
flag = b'slashroot6{'
while True:
    for c in range(16, 128):
        temp = flag + long_to_bytes(c)
        r.recvuntil(b": ")
        r.sendline(b'2')
        r.recvuntil(b": ")
        r.sendline(temp)
        r.recvuntil(b": ")
        ctTemp = r.recvline()[:-1]
        if(ctTemp == ct[:len(ctTemp)]):
            flag = temp
            break
        if(c==127):
            print(flag)
            print("error")
            exit()
    if flag[-1]==b'}':
        print(flag)
        break
r.interactive()
```

Flag: `slashroot6{rc_Rc_RC_Rc_1s_Rc4_3ncryp7ion_101!!!!!!}`

## Takoyaki

```py
from pwn import * # pip install pwntools
import json
import codecs
from Crypto.Util.number import long_to_bytes

ip = "103.152.242.37"
#sock = int

sock = 10101

r = remote(ip, sock, level = "debug")

r.recvuntil(b": ")
n = int(r.recvline()[:-1].decode())
r.recvuntil(b": ")
e = int(r.recvline()[:-1].decode())
r.recvuntil(b": ")
c = int(r.recvline()[:-1].decode())
inv2 = pow(2, e, n)
payload = inv2*c
r.recvuntil(b"> ")
r.sendline(str(payload).encode())

r.recvuntil(b": ")
ct = int(r.recvline()[:-1].decode())

flag = ct * pow(2,-1,n) % n
print(long_to_bytes(flag))
```

Flag: `slashroot6{R5A_ar3_D3licious_l1ke_Tak0Y4ki}`

# Forensic

## RRQ

1. Use wireshark to sniff packet
2. get 25 image
3. satuin
4. stonks

Flag: `slashroot6{sn1ffing_pc4p_is_fun}`
