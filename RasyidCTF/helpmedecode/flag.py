#!/usr/bin/env python2

flag = ">OAMva,mnoZo,h.Z.i^mtkoZ,iZktoc+i:x"
encrypted = ""
for x in flag:
    encrypted += chr(ord(x) + 0x0000000005 % 0xFFFFFFFFFFF)

print encrypted
