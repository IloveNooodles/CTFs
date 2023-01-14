import random
from string import digits, ascii_uppercase

FLAG = "REDACTED"

def generate_key(key_length: int, seed_length: int):

    str_seeder = ''.join(random.choices(digits, k = seed_length))
    random.seed(str_seeder)

    return "".join(random.choices(ascii_uppercase, k = key_length))

def encrypt():

    key = generate_key(len(FLAG), 4)
    result = []

    for idx, value in enumerate(FLAG):
        
        ciphertext = (ord(value)*2) + (ord(key[idx])*3)

        result.append(ciphertext.to_bytes(2, 'little'))

    with open('output.txt', 'wb') as writing_file:
        
        writing_file.write(b''.join(result))

if __name__ == '__main__':
    encrypt()
