from http import HTTPStatus
from incoming import requests
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):

    def remember_request(self):
        requests.put({
            'path': self.path,
            'method': self.command
        })

    def do_ALL(self):
        self.remember_request()

        # Forward the request to app
        client = HTTPConnection('localhost', self.app_port)
        client.request(self.command, self.path)
        response = client.getresponse()

        # Forward the response to client
        self.send_response(response.status)
        self.end_headers()
        self.wfile.write(response.read())

    def send_error(self, code, message=None, explain=None):
        # Intercept not implemented error to support all methods.
        if code == HTTPStatus.NOT_IMPLEMENTED:
            self.do_ALL()
        else:
            super().send_error(code, message, explain)
