from scapy.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import time

# AES Key
KEY = bytes.fromhex("546869734973415365637265744b6579")
cipher = AES.new(KEY, AES.MODE_ECB)

# Server
host = "chamber-of-echos.challenges.beginners.seccon.jp"

# Collected parts
flag_parts = {}


def decrypt_block(block: bytes) -> str:
    try:
        decrypted = cipher.decrypt(block)
        plaintext = unpad(decrypted, 16)
        return plaintext.decode()
    except Exception:
        return None


print("[*] Starting ICMP ping flood...")

while True:
    pkt = sr1(IP(dst=host) / ICMP(), timeout=1, verbose=0)
    if pkt and Raw in pkt:
        enc_chunk = pkt[Raw].load
        dec = decrypt_block(enc_chunk)
        if dec and "|" in dec:
            index, data = dec.split("|", 1)
            if index.isdigit():
                index = int(index)
                if index not in flag_parts:
                    flag_parts[index] = data
                    print(f"[+] Got chunk {index}: {data}")

    if len(flag_parts) >= 10:  # Adjust if you expect more/less
        break
    time.sleep(0.1)

# Reassemble the flag
flag = "".join(flag_parts[i] for i in sorted(flag_parts))
print(f"\n[🎉] FLAG: {flag}")

# [+] Got chunk 1: c0v3rt_ch4nn3l
# [+] Got chunk 0: ctf4b{th1s_1s_c0v3rt_ch4nn3l_4tt4ck}
# [+] Got chunk 2: _4tt4ck}
