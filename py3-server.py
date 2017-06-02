#!/usr/bin/python3

import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import base64

hostName = ""
hostPort = 59981


class BaseAuthHTTPRequestHandler(BaseHTTPRequestHandler):
    """
        BaseAuthHTTPRequestHandler
        Base Auth HTTP Handler
    """
    users = {
        'test': 'test',
        'dev': 'dev'
    }

    def _pre_auth(self):
        """
        pre_auth
        """
        authorization = self.headers.get('authorization')

        if (authorization is None) or (not authorization.startswith('Basic ')):
            print("Authorization Failed - None")
            self.do_AUTHHEAD()
        else:
            authorization_token = authorization.split(" ")[1]
            authorization_token_bytes = authorization_token.encode()
            decoded_token = bytes.decode(base64.b64decode(authorization_token_bytes))
            user, password = tuple(decoded_token.split(":"))
            if self.users[user] == password:
                # test:test
                print("Authorization succeeded - SUCCESS")
                self.do_HEAD()
            else:
                print("Authorization Failed - nonsense provided")
                self.do_AUTHHEAD()

    def do_HEAD(self):
        """
            do_HEAD
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        """
            do_AUTHHEAD
        """
        # print("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Local Authentication. Try test:test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """
            do_GET
        """
        self._pre_auth()
        self.send_response(200)
        self.wfile.write(bytes("You accessed path: %s" % self.path, "utf-8"))

    def do_POST(self):
        """
            do_POST
        """

        self._pre_auth()
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)  # <--- Gets the data itself
        print("incoming http: ", post_data)
        self.send_response(200)
        self.wfile.write(bytes("You posted this: %s" % post_data, "utf-8"))


base_auth_handler = BaseAuthHTTPRequestHandler
customWebServer = HTTPServer((hostName, hostPort), base_auth_handler)
print(time.asctime(), "Server Starts - %s:%s" % (hostName, hostPort))

try:
    customWebServer.serve_forever()
except KeyboardInterrupt:
    pass

customWebServer.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (hostName, hostPort))
