f = open("flag.jpg", "rb")
data = f.read()
print(len(data))

# JPG = b"\xFF\xD7\xFF\xE0\x00\x10\x4A\x46\x49\x46"
# b = data.split(JPG)
# print(b)

# file1 = JPG + b[1]
# file2 = JPG + b[2]

# f1 = open("img1.jpg", "wb")
# f1.write(file1)
# f1.close()

# f2 = open("img2.jpg", "wb")
# f2.write(file2)
# f2.close()
