from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
from socketserver import ThreadingMixIn
from random import randint
from urllib.request import urlopen
import ssl, json, cgi, threading, os

hostName = "0.0.0.0"
serverPort = 8000
sessions = {}

def send(data):
    forbidden = {
        "<":"&lt;",
        ">":"&gt;",
    }
    for _, x in forbidden.items():
        data = data.replace(_, x)
    return data

class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        ip = self.client_address
        print(ip[0])
        if self.path == '/check':
            self.cookie = None
            cookies = self.parse_cookies(self.headers["Cookie"])
            if "sid" in cookies:
                self.loggedin = cookies["sid"] if (cookies["sid"] in sessions) else False
                self.send_response(200)
            else:
                sid = self.generate_sid()
                self.cookie = f"sid={sid}; SameSite=None; Secure"
                sessions[sid] = {"username":"guest"}
                self.loggedin = False

                self.send_response(200)
                self.send_header('Set-Cookie', self.cookie)

            # TODO
            if self.client_address[0] == "172.10.0.69":
                self.send_header('Set-Cookie', f"FLAG={os.environ['FLAG']}; SameSite=Lax; Secure")

            self.send_header('Content-Security-Policy', "script-src https://cdnjs.cloudflare.com 'unsafe-eval'; object-src 'none';")
            self.end_headers()
            
            if self.loggedin:
                self.wfile.write(f'<b>Hello {sessions[cookies["sid"]]["username"]}!</b>'.encode())
            else:
                self.wfile.write(f'<b>Hello guest!</b>'.encode())
            return
        else:
            return super().do_GET()

    def do_POST(self):
        if self.path == '/api':
            if "application/json" not in self.headers['Content-Type']:
                self.send_response(415)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<b> 415 Unsupported Media Type! </b>")
                return
            else:
                file_length = int(self.headers['Content-Length'])
                data = json.loads(send((self.rfile.read(file_length)).decode()))

                # TODO
                if self.client_address[0] == "172.10.0.69":
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(f"Under Maintenance!".encode())
                    cookies = self.parse_cookies(self.headers["Cookie"])
                    self.loggedin = cookies["sid"] if (cookies["sid"] in sessions) else False
                    if self.loggedin:
                        sessions[cookies["sid"]]["username"] = data["name"]
                else:
                    self.send_response(401)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b"<b> 401 Unauthorized! </b>")
                return

    def generate_sid(self):
        from hashlib import md5
        return md5("".join(str(randint(1,9)) for _ in range(100)).encode()).hexdigest()

    def parse_cookies(self, cookie_list):
        return dict(((c.split("=")) for c in cookie_list.split(";"))) \
        if cookie_list else {}

if __name__ == "__main__":        
    httpd = ThreadingSimpleServer((hostName, serverPort), Handler)
    httpd.timeout = 2 # idk if its actually works
    sslctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    sslctx.check_hostname = False
    sslctx.load_cert_chain(certfile='ssl_stuff/certificate.pem', keyfile="ssl_stuff/private.pem")
    httpd.socket = sslctx.wrap_socket(httpd.socket, server_side=True)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")