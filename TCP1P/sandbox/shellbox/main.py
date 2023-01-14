from subprocess import check_output

def decode_base64(txt):
    base = check_output(f"echo '{txt}' | base64", shell=True)
    return base.decode()

with open("logo", "r") as f:
    print(f.read())

print("Selamat datang di aplikasi encode base64 by Byt3T4G0r3!")
user_input = input("Masukkan text: ")
base64 = decode_base64(user_input)
print(f"Hasil: {base64}")