from pwn import * # pip install pwntools
import json
import codecs
from Crypto.Util.number import long_to_bytes

# nc 103.250.10.198 31337
r = remote('103.250.10.198', 31337, level = 'debug')


i = 0
payload = "00000-00000-00000-00000-"
while True:
    ans = r.recvuntil(b'[>] Enter License: ')
    if "[+] Flag:" in ans.decode() or "[!]" in ans.decode():
        print(ans)
        break
    temp = payload + f"{i:05}"
    r.wait(0.91)
    r.sendline(temp.encode())
    i+=1