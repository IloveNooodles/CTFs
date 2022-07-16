# #1
# def gcd(a, b):
#   if b == 0:
#     return a
#   else:
#     return gcd(b, a%b)

# print(gcd(66528, 52920))

#2
def exgcd(a, b):
  if b == 0:
    x = 1
    y = 0
    return a, 1, 0
  
  gcd, x1, y1 = exgcd(b, a%b)
  print(x1, y1)
  x = y1
  y = x1 - (a//b) * y1

  return gcd, x, y

gcd, x, y = exgcd(26513, 32321)
print(x, y)