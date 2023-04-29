key = "EKMGAWZULN"
text = "UFJOXJGWSH"
dec = "QVXIXNHCHU"
chars = [chr(ord("A") + i) for i in range(26)]

for a,b in zip(key, text):
    posa = chars.index(a)
    posb = chars.index(b)
    l = (posb-posa-posa-posa) % 26
    print(chars[l], end="")