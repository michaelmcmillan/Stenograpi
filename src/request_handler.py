from http import HTTPStatus
from http.client import HTTPConnection
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):

    def remember_request(self):
        self.bucket.add({
            'path': self.path,
            'method': self.command
        })

    def do_ALL(self):
        self.remember_request()

        # Don't send a request if port is unspecified
        if not self.app_port:
            return

        # Forward the request to app
        client = HTTPConnection('localhost', self.app_port)
        client.request(self.command, self.path)
        response = client.getresponse()

        # Forward the response to client
        self.send_response(response.status)
        self.end_headers()
        self.wfile.write(response.read())

    def send_error(self, code, message=None, explain=None):
        # This error will always occur upon receiving a request. To
        # support all HTTP verbs we ironically avoid any "DO_VERB"
        # methods in this class to trigger this error. We proceed
        # by calling our "catch-all" handler called "DO_ALL".
        if code == HTTPStatus.NOT_IMPLEMENTED:
            self.do_ALL()
        else:
            super().send_error(code, message, explain)

    def log_message(self, *args):
        return
