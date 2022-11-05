from Crypto.Util.number import long_to_bytes


def append(des, src):
    des += src
    return des


def strcpy_offset(src, start, end):
    return src[start:end]


val1 = 0x65625F73695F7373
val2 = 0x5F73695F73737375
val3 = 0x74735F6573756562
val4 = 0x7473695F72657474
val5 = 0x6972695F72657474
val6 = 0x6575675F685F676E

dest = b""
dest += (
    long_to_bytes(val1)
    + long_to_bytes(val2)
    + long_to_bytes(val3)
    + long_to_bytes(val4)
    + long_to_bytes(val5)
    + long_to_bytes(val6)
)

before = dest.decode()

# final_input = dest.decode()
# inter1 = strcpy_offset(final_input, 0, 6)
# inter2 = strcpy_offset(final_input, 6, 0xC)
# inter3 = strcpy_offset(final_input, 0xC, 0x12)
# inter4 = strcpy_offset(final_input, 0x12, 0x18)
# inter5 = strcpy_offset(final_input, 0x18, 0x1E)

# print("before:", before)
# print(len(inter1) + len(inter2) + len(inter3) + len(inter4) + len(inter5))

# inter1 = append(inter1, inter4)
# inter2 = append(inter2, inter5)
# inter3 = append(inter3, inter1)
# inter2 = append(inter2, inter3)

# print("After: ", inter2, len(inter2))

# final_input = inter2

# inter_1 = strcpy_offset(final_input, 0, 10)
# inter_2 = strcpy_offset(final_input, 10, 0x14)
# inter_3 = strcpy_offset(final_input, 0x14, 0x1E)

# inter_3 = append(inter_3, inter_1)
# inter_2 = append(inter_2, inter_3)

# print("final: ", inter_2)

inter_2_3_1 = before
print(len(before))
print("start", inter_2_3_1)

inter_2 = inter_2_3_1[:10]
inter_3 = inter_2_3_1[10:20]
inter_1 = inter_2_3_1[20:30]

inter_2_5_3_1_4 = inter_1 + inter_2 + inter_3
print("rev1: ", inter_2_5_3_1_4)

inter_2 = inter_2_5_3_1_4[0:6]
inter_5 = inter_2_5_3_1_4[6:12]
inter_3 = inter_2_5_3_1_4[12:18]
inter_1 = inter_2_5_3_1_4[18:24]
inter_4 = inter_2_5_3_1_4[24:30]

first_input = inter_1 + inter_2 + inter_3 + inter_4 + inter_5
print(first_input)