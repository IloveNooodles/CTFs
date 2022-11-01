a = open("chall.txt")

b = a.read().split(" ")
print(b)

for char in b:
    print(chr(int(char)), end="")
