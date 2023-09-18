from z3 import *

flag = [Int(f'{i}') for i in range(48)]

s = Solver()

s.add(flag[22]-flag[28]+flag[4]+flag[35]-flag[29] == -25)
s.add(flag[26]-flag[0]+flag[23]+flag[11]-flag[16] ==-19)
s.add(flag[9]-flag[21]+flag[37]+flag[34]-flag[14]==195)
s.add(flag[19]-flag[18]+flag[6]+flag[13]-flag[12]==112)
s.add(flag[36]-flag[38]+flag[33]+flag[32]-flag[3]==168)
s.add(flag[2]-flag[20]+flag[7]+flag[10]-flag[30]==49)
s.add(flag[5]-flag[25]+flag[27]+flag[39]-flag[17]==87)
s.add(flag[24]-flag[8]+flag[15]+flag[31]-flag[1]==102)
s.add(flag[22]+flag[28]-flag[4]-flag[35]+flag[29]==105)
s.add(flag[26]+flag[0]-flag[23]-flag[11]+flag[16]==83)
s.add(flag[9]+flag[21]-flag[37]-flag[34]+flag[14]==49)
s.add(flag[19]+flag[18]-flag[6]-flag[13]+flag[12]==122)
s.add(flag[36]+flag[38]-flag[33]-flag[32]+flag[3]==-96)
s.add(flag[2]+flag[20]-flag[7]-flag[10]+flag[30]==147)
s.add(flag[5]+flag[25]-flag[27]-flag[39]+flag[17]==123)
s.add(flag[24]+flag[8]-flag[15]-flag[31]+flag[1]==120)
s.add(flag[22]-flag[28]-flag[4]+flag[35]+flag[29]==-47)
s.add(flag[26]-flag[0]-flag[23]+flag[11]+flag[16]==-37)
s.add(flag[9]-flag[21]-flag[37]+flag[34]+flag[14]==223)
s.add(flag[19]-flag[18]-flag[6]+flag[13]+flag[12]==136)
s.add(flag[36]-flag[38]-flag[33]+flag[32]+flag[3]==28)
s.add(flag[2]-flag[20]-flag[7]+flag[10]+flag[30]==41)
s.add(flag[5]-flag[25]-flag[27]+flag[39]+flag[17]==-27)
s.add(flag[5]-flag[25]-flag[27]+flag[39]+flag[17]==-27)
s.add(flag[24]-flag[8]-flag[15]+flag[31]+flag[1]==90)
s.add(flag[22]+flag[28]+flag[4]-flag[35]-flag[29]==127)
s.add(flag[26]+flag[0]+flag[23]-flag[11]-flag[16] ==101)
s.add(flag[9]+flag[21]+flag[37]-flag[34]-flag[14]==21)
s.add(flag[19]+flag[18]+flag[6]-flag[13]-flag[12]==98)
s.add(flag[36]+flag[38]+flag[33]-flag[32]-flag[3]==44)
s.add(flag[2]+flag[20]+flag[7]-flag[10]-flag[30]==155)
s.add(flag[5]+flag[25]+flag[27]-flag[39]-flag[17]==237)
s.add(flag[24]+flag[8]+flag[15]-flag[31]-flag[1]==132)
s.add(flag[22]-flag[28]+flag[4]-flag[35]+flag[29]==105)
s.add(flag[26]-flag[0]+flag[23]-flag[11]+flag[16]==93)
s.add(flag[9]-flag[21]+flag[37]-flag[34]+flag[14]==173)
s.add(flag[19]-flag[18]+flag[6]-flag[13]+flag[12]==134)
s.add(flag[36]-flag[38]+flag[33]-flag[32]+flag[3]==64)
s.add(flag[2]-flag[20]+flag[7]-flag[10]+flag[30]==153)
s.add(flag[5]-flag[25]+flag[27]-flag[39]+flag[17]==95)
s.add(flag[24]-flag[8]+flag[15]-flag[31]+flag[1]==262)
s.add(flag[22]+flag[28]-flag[4]+flag[35]-flag[29]==-25)
s.add(flag[26]+flag[0]-flag[23]+flag[11]-flag[16]==-29)
s.add(flag[9]+flag[21]-flag[37]+flag[34]-flag[14]==71)
s.add(flag[19]+flag[18]-flag[6]+flag[13]-flag[12]==100)
s.add(flag[36]+flag[38]-flag[33]+flag[32]-flag[3]==8)
s.add(flag[2]+flag[20]-flag[7]+flag[10]-flag[30]==43)
s.add(flag[5]+flag[25]-flag[27]+flag[39]-flag[17]==115)
s.add(flag[24]+flag[8]-flag[15]+flag[31]-flag[1]==-40)
s.add(flag[22]-flag[28]-flag[4]-flag[35]-flag[29]==-305)
s.add(flag[26]-flag[0]-flag[23]-flag[11]-flag[16]==-329)
s.add(flag[9]-flag[21]-flag[37]-flag[34]-flag[14]==-231)
s.add(flag[19]-flag[18]-flag[6]-flag[13]-flag[12]==-330)
s.add(flag[36]-flag[38]-flag[33]-flag[32]-flag[3]==-260)
s.add(flag[2]-flag[20]-flag[7]-flag[10]-flag[30]==-267)
s.add(flag[5]-flag[25]-flag[27]-flag[39]-flag[17]==-199)
s.add(flag[24]-flag[8]-flag[15]-flag[31]-flag[1]==-198)
s.add(flag[22]+flag[28]+flag[4]+flag[35]+flag[29]==385)
s.add(flag[26]+flag[0]+flag[23]+flag[11]+flag[16]==393)
s.add(flag[9]+flag[21]+flag[37]+flag[34]+flag[14]==475)
s.add(flag[19]+flag[18]+flag[6]+flag[13]+flag[12]==564)
s.add(flag[36]+flag[38]+flag[33]+flag[32]+flag[3]==332)
s.add(flag[2]+flag[20]+flag[7]+flag[10]+flag[30]==463)
s.add(flag[5]+flag[25]+flag[27]+flag[39]+flag[17]==409)
s.add(flag[24]+flag[8]+flag[15]+flag[31]+flag[1]==420)

print(s.check())
print(s.model())

ans = {39: 41,
 7: 107,
 28: 108,
 38: 36,
 27: 102,
 35: 32,
 37: 94,
 6: 110,
 11: 45,
 25: 116,
 33: 116,
 8: 47,
 0: 105,
 4: 108,
 18: 104,
 20: 104,
 34: 119,
 31: 32,
 32: 98,
 13: 111,
 10: 51,
 21: 32,
 15: 118,
 23: 110,
 24: 111,
 5: 105,
 2: 98,
 36: 36,
 19: 117,
 9: 122,
 26: 32,
 22: 40,
 1: 112,
 17: 45,
 30: 103,
 3: 46,
 12: 122,
 14: 108,
 16: 101,
 29: 97}
for i in range(40):
  print(chr(ans[i]), end= "")