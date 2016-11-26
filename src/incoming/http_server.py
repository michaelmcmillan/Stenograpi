from http.server import HTTPServer
from socketserver import ThreadingMixIn
from incoming.request_handler import RequestHandler

class PythonHTTPServer(ThreadingMixIn, HTTPServer):

    def __init__(self, host, port, app_port):
        RequestHandler.app_port = app_port
        super().__init__((host, port), RequestHandler)
