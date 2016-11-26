from http.server import HTTPServer
from socketserver import ThreadingMixIn
from request_handler import RequestHandler

class PythonHTTPServer(ThreadingMixIn, HTTPServer):

  def __init__(self, host, port):
      super(PythonHTTPServer, self).__init__((host, port), RequestHandler)
