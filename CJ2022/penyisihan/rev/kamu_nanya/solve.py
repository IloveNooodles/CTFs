flag = []
for i in range(590):
    filename = './bertanya{}'.format(str(i))
    f = open(filename, "rb")
    data = f.read()
    ops = ord(data[202])
    by = ord(data[203])
    comparsion = ord(data[206])
    f.close()

    if ops == 0xea: # sub
      flag.append(comparsion+by)
  
    if ops == 0xc2: # add
      flag.append(comparsion-by)

    if ops == 0xf2: # xor
      flag.append(comparsion^by)

print(''.join([chr(x&0xff) for x in flag]))