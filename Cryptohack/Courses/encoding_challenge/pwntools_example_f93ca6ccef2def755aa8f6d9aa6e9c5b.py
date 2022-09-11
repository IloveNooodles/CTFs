from Crypto.Util.number import bytes_to_long, long_to_bytes
from base64 import decode
from pwn import *  # pip install pwntools
import codecs
import json

r = remote('socket.cryptohack.org', 13377, level='debug')


def json_recv():
    line = r.recvline()
    return json.loads(line.decode())


def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)


received = json_recv()
for i in range(101):
    encoded_type = received["type"]
    encoded_string = received["encoded"]
    print("Received type: ")
    print(encoded_type)
    print("Received encoded value: ")
    print(encoded_string)

    decoded_str = ""

    if encoded_type == "base64":
        decoded_str = base64.b64decode(encoded_string).decode()
        print(decoded_str)
    elif encoded_type == "hex":
        decoded_str = unhex(encoded_string).decode()
    elif encoded_type == "rot13":
        decoded_str = codecs.decode(encoded_string, "rot13")
    elif encoded_type == "bigint":
        decoded_str = long_to_bytes(int(encoded_string, 16)).decode()
    elif encoded_type == "utf-8":
        decoded_str = "".join([chr(y) for y in encoded_string])

    print(decoded_str)

    to_send = {
        "decoded": decoded_str
    }
    json_send(to_send)

    received = json_recv()
