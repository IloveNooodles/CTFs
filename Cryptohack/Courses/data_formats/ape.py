from Crypto.PublicKey import RSA

# 1
# f = open("privacy.pem", 'r')

# key = RSA.importKey(f.read())

# print(key.d)


# 2
# - convert to pem using openssl
# - use the method from no 1
# openssl x509 -inform DER -in 2048b-rsa.der > 2048b.pem

# f = open("2048b.pem", 'r')

# key = RSA.importKey(f.read())

# print(key.n)


# 3
# f = open("bruce_rsa.pub", 'r')

# key = RSA.importKey(f.read())

# print(key.n)

# 4
f = open("trans.pem", 'r')

key = RSA.importKey(f.read())

print(key.)
