import secrets


def random():
    return secrets.choice([i for i in range(100)])


def main():
    point = 0
    try:
        for _ in range(100):
            ya = False
            server = random()
            for _ in range(7):
                client = int(input("mana? "))
                if client != server:
                    if client < server:
                        print("apah?")
                    else:
                        print("huh?")
                else:
                    print("good job!!!")
                    ya = True
                    break
            if ya:
                point += 1
            else:
                print("good bye!!!")
                exit()
    except:
        print("something wrong!")
    if point == 100:
        print("REDACTED")


if __name__ == "__main__":
    main()
