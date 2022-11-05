pika1 = open("./pikachu.jpg", "rb")
pika2 = open("./pikachu.png", "rb")

for b in pika1.read():
    for c in pika2.read():
        if b != c:
            print("b, c: ", b, " ", c)