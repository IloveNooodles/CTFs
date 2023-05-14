import numpy as np

f = open("write.txt", "w")


def solve():
    f = open("cmd.txt")
    ans = ""
    for line in f.readlines():
        curr_pos = [7, 0]
        zeroes = np.zeros((8, 16))
        zeroes[curr_pos[0]][curr_pos[1]] = 1
        for char in line:
            if char == 'u':
                curr_pos[0] -= 1
            elif char == 'd':
                curr_pos[0] += 1
            elif char == 'r':
                curr_pos[1] += 1
            elif char == 'l':
                curr_pos[1] -= 1
            try:
                zeroes[curr_pos[0]][curr_pos[1]] = 1
            except:
                pass

        print(zeroes)
        print()


solve()
