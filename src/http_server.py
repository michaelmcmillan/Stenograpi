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
