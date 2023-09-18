txt = open("./helper.py", "r").read()
flag = open("./important_file.hackedlol", "rb").read()

for idx in range(len(flag)):
  print(chr(flag[idx] ^ ord(txt[(idx*0x27) % len(txt)])),end="")