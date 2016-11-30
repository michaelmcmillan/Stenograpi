from http.server import HTTPServer
from socketserver import ThreadingMixIn
from request_handler import RequestHandler

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
from request import Request
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
            return self.bucket.get(block=True, timeout=15)
        except Empty:
            return None
#pylint: disable=W0221
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

        # Obain the response
        response = client.getresponse()

        # Forward the response to client
        self.send_response(response.status)
        for key, value in response.headers.items():
            self.send_header(key, value, True)
        self.end_headers()
        self.wfile.write(response.read())

    def send_header(self, key, value, it_is_us=False):
        # We override this method with an additional flag. This is
        # to avoid the Base class sending HTTP headers on our behalf.
        # For instance "Server: BaseHTTP/0.6 Python/3.5.1".
        if it_is_us:
            super().send_header(key, value)

    def send_error(self, code, message=None, explain=None):
        # This error will always occur upon receiving a request. To
        # support all HTTP verbs we ironically avoid any "DO_VERB"
        # methods in this class to trigger this error. We sidestep
        # the error handling by calling our "catch-all" method "DO_ALL".
        if code == HTTPStatus.NOT_IMPLEMENTED:
            self.do_ALL()
        else:
            super().send_error(code, message, explain)

    def log_message(self, *args):
        return
from threading import Thread
from http_server import PythonHTTPServer
from request_bucket import RequestBucket

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
from sys import argv
from argparse import ArgumentParser

def parse_args(args):
    parser = ArgumentParser(prog='stenograpi.py',
                            description='Document your HTTP API automatically through tests.')

    parser.add_argument('hostname', type=str, help='hostname of Stenograpi')
    parser.add_argument('port', type=int, help='port Stenograpi should listen on')

    parser.add_argument('app-hostname', type=str, help='hostname of your app')
    parser.add_argument('app-port', type=int, help='port your app is listening on')
    return parser.parse_args(args)

if __name__ == '__main__':
    args = parse_args(argv[1:])
    stenograpi = Stenograpi(args.hostname, args.port, getattr(args, 'app-port'))
    stenograpi.listen()
    request = stenograpi.get_latest_request()
    print(request)
