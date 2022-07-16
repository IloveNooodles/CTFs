f = open('./message.txt')
alph = 'abcdefghijklmnopqrstuvwxyz'
string = ''
for line in f:
  print(alph[(len(line.split()))-1], end = '')
