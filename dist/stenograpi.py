from http.server import HTTPServer
from socketserver import ThreadingMixIn

class PythonHTTPServer(ThreadingMixIn, HTTPServer):

    def __init__(self, bucket, host, port, app_port):
        RequestHandler.bucket = bucket
        RequestHandler.app_port = app_port
        super().__init__((host, port), RequestHandler)

    def get_port(self):
        return self.socket.getsockname()[1]

    def close(self):
        return self.socket.close()
class Request:

    def __init__(self):
        self.path = None
        self.method = None
from queue import Queue, Empty

class RequestBucket:

    def __init__(self):
        self.bucket = Queue()

    def add(self, incoming_request):
        request = Request()
        request.path = incoming_request['path']
        request.method = incoming_request['method']
        self.bucket.put(request)

    def get_latest_request(self):
        try:
            return self.bucket.get(block=True, timeout=0.010)
        except Empty:
            return None
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
from argparse import ArgumentParser

parser = ArgumentParser(prog='stenograpi.py',
                        description='Document your HTTP API automatically through tests.')

parser.add_argument('--hostname', type=str, help='hostname of Stenograpi')
parser.add_argument('--port', type=int, help='port Stenograpi should listen on')

parser.add_argument('--app-hostname', type=str, help='hostname of your app')
parser.add_argument('--app-port', type=int, help='port your app is listening on')

if __name__ == '__main__':
    arguments = parser.parse_args()
from threading import Thread

class Stenograpi:

    def __init__(self, host, port, app_port):
        self.bucket = RequestBucket()
        self.server = PythonHTTPServer(self.bucket, host, port, app_port)
        self.thread = Thread(target=self.server.serve_forever)

    def listen(self):
        self.thread.daemon = True
        self.thread.start()

    @property
    def port(self):
        return self.server.get_port()

    def shutdown(self):
        self.server.close()

    def get_latest_request(self):
        return self.bucket.get_latest_request()
