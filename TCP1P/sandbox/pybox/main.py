def calculator(txt: str):
    txt = txt.replace("=", "")
    return eval(txt)

with open("logo", 'r') as f:
    print(f.read())

print("aplikasi aritmatika by H3X0S1337")
print("operasi yang bisa digunakan: ")
print("- perkalian '*'")
print("- pembagian '/'")
print("- pertambahan '+'")
print("- pengurangan '-'")
print("- xor '^'")
print("- modulus '%'")
print("- pangkat '**'")
print("- pembagian lantai '//'")
print("contoh pemakaian:")
print("- 1+1 maka akan menghasilkan 2")
while True:
    try:
        user_input = input("masukkan input: ")
        calc = calculator(user_input)
        print(calc)
    except KeyboardInterrupt:
        break