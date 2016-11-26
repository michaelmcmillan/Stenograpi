from requests import requests
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):

    def remember_request(self):
        requests.put({ 'path': self.path, 'method': self.command })

    def send_error(self, code, message=None, explain=None):
        # Intercept not implemented error to support all methods.
        if code == HTTPStatus.NOT_IMPLEMENTED:
          self.remember_request()
        else:
          return super(RequestHandler, self).send_error(code, message, explain)
