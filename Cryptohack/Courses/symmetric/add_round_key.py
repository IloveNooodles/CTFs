from operator import xor


state = [
    [206, 243, 61, 34],
    [171, 11, 93, 31],
    [16, 200, 91, 108],
    [150, 3, 194, 51],
]

round_key = [
    [173, 129, 68, 82],
    [223, 100, 38, 109],
    [32, 189, 53, 8],
    [253, 48, 187, 78],
]


def add_round_key(s, k):
    new_state = []
    for i in range(4):
        for j in range(4):
            new_state.append(xor(s[i][j], k[i][j]))
    return new_state


# def matrix2bytes(matrix):
#     str = ""
#     for i in range(len(matrix)):
#         for j in range(len(matrix[0])):
#             str += chr(matrix[i][j])
#     return str


c = add_round_key(state, round_key)
str = ""
for i in range(16):
  str += chr(c[i])

print(str)