import re
from string import ascii_lowercase, ascii_uppercase, digits

import bs4
import requests

arr = []
bs = bs4.BeautifulSoup()

session = requests.session()

cookie = {
  "session": "1250efec-8d13-469b-a183-85b2b5497d58.Kui4Hfv_JOknekwXc2ysSBLySxc",
  "PHPSESSID": "9fdaf1f8ca7f5d94625f7b661038a9b5"
}

weird = ['5NBWXRGUS9WRSL8WSIUT', '', '2NHO7F027JSVLC9JA00V', '5HVAEV6VVMADR5EVS2VB', 'JQM5DVNEFIXQ42DNVDEU', 'WR78YR2UHPGJFNK50F29', 'PCY0LWJW0SCWJLOJ7R8J', 'VV6QZPA1R92HVO4VOY46', 'IZVXKC3HADCGC8SNAJI8', '72Q21A7D7TT3BUJD51OL', '1NWVG408EPU9NHJPG6BX', 'A5R59N6W057JULSOJI3N', 'RY9ZF1UCTHOBSBN1PXAW', 'BKN8LPZBCGJDUBN00UJU', 'Z72RCOEHLWELOHBW0592', '5NBWXRGUS9WRSL8WSIUT', '9AK4688MUA3OQNGWHD9L', 'GC7PNI9UMZLZ6NFO5GXI', 'AMQT3MXQSKIPTQU1778Q', 'TV6397O0K5GFUSJRXMI8', '4H07SFSKTX6O3O2RGY0N', 'NTGKL5TSZQBQP0MUIXI1', 'JSRNTBLWME1BRCZE22MP', 'QZU3LBQBGRMULI5H5KXP', 'C5Q1LEH0QISD153NNI2A', 'UMJ2G078MSYJF2ZCPXLP', '5J718Z5NC2MBK272PTIC', 'GGMXWR0GFD7P5IMADVO2', '6O8G3R45IDKFI8VH846F', 'YHXZWIUJHN8U0SV7GMKF', 'Q9BH2DJO4B2I9IBF8J04', 'ULKHMLL9E8SDZQ0MTYGE', '5BTJRWL6UPSY8KRIYX2W', 'NIGL6J1ZTY03826FSO94', '868H1YDT1Y362SK82IYO', 'RXGG0GUTIK58VL20RTTS', '7LY7PQT44FUTHWES25NA', 'TIK219JM3KLOJLQOELEH', '6WGJ53PLTSI7NQXFVAD9', 'Z54UWFUOTY0FLP729QLO', 'M2FC46WXTU1P0E0X7L50', 'GLOEKH5VXBCV9GWAG3YT', 'KBZRC99WH9A77HIUQTMD', 'RNNB9EYZLAP1HYGQYHXK', 'PZ1YVCQO9GY161XXN0WL', 'Jono chef yang paling ganteng, saya biasa menggunakan TechnoFairCTF{Sp1cy_P3pp3r_\r\ndan sisa nya ada di ... Flag collected (1/2)\r\n', '7VRAOEH1WWEOIIATA1G6', 'FR8G7FBVQ3LV72QTWDJ3', 'VX690TLOV46Y5JU95F94', '9HOGMRG41LUAUYB8GCF6', 'PEN1FMV0LBOK92X13L19', 'CO305T2TQ3GZ2UK9FJJX', 'GHWQGRD6DPJPD5CXN0SU', 'JFGJ2OIABXHBG5NIL8KI', 'QEROVW6XQEX2A5XIH1E7', '8GZO3I2Z07BEJ4NBDMGE', 'OEERSU4YDYUN9KLH9EWC', 'PNS65JDOJ454KGWTKCFQ', 'U7LEW8NP3NCBGSA40G62', '1VBTQMCUQKDQWX3Z0VVX', '7XXK4N0QL1LIYTNGU30S', '4D8UEXVVFKLATSROVG2S', 'T1WNVO2XB36FB034LLZG', 'EUN7LQL4Z8K72E91OOBA', '9AOGXTRW1SIAY36O7IW3', '84PKZPUBU4OE6RT70ICY', '7LHF7WM9HOPW5H0BDT3N', 'S4EP17XTAY4UDDDY9QCY', 'A742XS075UH7OA77GRMS', 'AOOFER8FSSNY0WZNZQA2', 'Sisa bumbu rahasia yang saya gunakan adalah\r\n4nd_G4rlic_Sauce}\r\nFlag collected (2/2)', '71DEUR9890INEPKDFLYH', 'FZONQP1GE01O07I1I77M', 
'CCXP3NENDGU062QQEQD8', '8EFO5KD4W37MK914OG9D', 'Z7KTLEU1EKSKP1K5S413', 'IT2YHSSOD73AGI4RI3CG', 'NARIS9YKGHSM4IPCFQG1', 'KO0SSQDT047N15S1VHCP', 'QEQ3Y7WU3NY87KQ4VT37', 'ISDXAZARVI097TNKNKJM', '31UF7AMVW36MPE6Y0VNX', 'GPJGW9GOXOXSP0KCJ4Q3', 'PHPSZHXWEBKAR7LZ0ZVC', 'Z39TAZZGGAGG0WNBISH8', 'G1UGBFMVF2OHOEIK731V', '5EHXFBLHJQ9IF1W5URXB', 'RO3F3I8RHBK4TF6ZE5E1', 'H1NGV4GU169U1PTM6HMR', 'HZP5DSVAS6MVK4M3UCB2', '99ALONJG6P06AP20PB1V', 'VOMRCJ3QI354OZ1GSS1Z', 'VUWZ15MHDEHY0EARQKGH', 'H7XONVW4Q8H57C1VUXF1', '7BAMPQASP8CBLYI0P6KQ', 'FIMR9B77ZFZM1OR2YEQV', 'V75AK8H8QA1B9C5NVFCR', 'YI82NW34MR82RRETHGFR', 'KIOB13NPPT8Z6ZR6MF82', '3MUBBET4N0Z2PPP1KN1C', 'Q8HW00UGKNMDTK4IF5DJ', 'PAFSM6T3W9PQXCTQJFQN']


for i in range(1, 103):
  BASE_URL = f"http://103.152.242.197:29807/user.php?id={i}"
  
  r = requests.get(BASE_URL, cookies=cookie)
  data = r.text
  soup = bs4.BeautifulSoup(data, 'html.parser')
  soup2 = soup.find("h2").getText()
  weird.append(soup2)
  

print(weird)


"""
TechnoFairCTF{Sp1cy_P3pp3r_4nd_G4rlic_Sauce}
"""