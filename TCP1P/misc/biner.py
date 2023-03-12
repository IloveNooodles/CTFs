from pwn import *

conn = "nc 167.71.212.18 64896".split(" ")
host = conn[1]
port = conn[2]

p = remote(host, port)


def recv():
    return p.recv().decode()


def send(number: int):
    p.sendline(str(number).encode("utf-8"))


point = 0

print(recv())
while point < 100:
    low = 0
    high = 100
    for i in range(7):
        mid = (low + high) // 2
        send(mid)
        respond = recv()
        if "apah" in respond:
            low = mid + 1
        elif "huh" in respond:
            high = mid - 1
        elif "good job" in respond:
            point += 1
            print(f"Point: {point}")
            break

    if point == 100:
        print(respond)
        p.recvall()

p.interactive()
