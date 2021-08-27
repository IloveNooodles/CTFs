# Import the pwntools library
# You can install this via pip install pwntools
from pwn import *

# To process local files
# r = process('./filename')

# To connect to a remote server via nc
r = remote('13.228.30.172', 10075)

# To receive a line of data (until it finds \n)
data = r.recvline()

# To receive data until it finds '='
data = r.recvuntil('=')

# Processing the question
question = data[:-2]

# ...

# Producing the answer
answer = '1337'

# To send input '1337' to the remote server
r.sendline(answer)

# To continue the connection interactively (just like using command-line nc)
r.interactive()