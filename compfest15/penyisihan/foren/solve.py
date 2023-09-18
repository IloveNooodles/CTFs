# ===== tahap 1
payload = open('./cat.png', 'rb').read()

num = 0
mp = {
  b"\x00\x00": 0,
  b"\x00\x01": 1,
  b"\x00\x10": 2,
  b"\x00\x11": 3,
  b"\x01\x00": 4,
  b"\x01\x01": 5,
  b"\x01\x10": 6,
  b"\x01\x11": 7,
  b"\x10\x00": 8,
  b"\x10\x01": 9,
  b"\x10\x10": 10,
  b"\x10\x11": 11,
  b"\x11\x00": 12,
  b"\x11\x01": 13,
  b"\x11\x10": 14,
  b"\x11\x11": 15,
}

txt = ""

for c in range(0, len(payload), 2):
    p = payload[c:c+2]
    txt += hex(mp[p])[2:]

f = open("./a.txt", "w")
f.write(txt)
print(txt)

# ==== TAHAP 2