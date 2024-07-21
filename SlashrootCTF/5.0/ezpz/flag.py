from pwn import *

#nc 103.145.226.170 2021
addr = "103.145.226.170"
PORT = "2021"
p = remote(addr, PORT)
