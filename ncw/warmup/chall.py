from Crypto.Util.number import *

# m = bytes_to_long(b'REDACTED')
# p = getPrime(1024)
# b = getPrime(256)
# print('p =', p)
# print('b =', b)
# print('c =', (m * b) % p)

p = 157298851576543822658375911784453045330998529812070536941308894589946728967164760268450525258591318978074508398017643844478919786389777717487832814149957912540519405689102360584032513702174173244722929569320792883923849532462564138818899848421774547221444440026273071418600547380652550004673222604837135280657
b = 103580599751196930634226832960307347818265788172966651313814056767115610483969
c = 240300149694030447007884123637429317743010940470695815765906818058157502481117145356755475103323590208098621089447994933914357246137429600996167409043078392957


print(long_to_bytes(c // b))