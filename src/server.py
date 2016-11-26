from queue import Empty
from request import Request
from requests import requests
from threading import Thread
from http_server import PythonHTTPServer

class StenograpiServer:

  def __init__(self, host, port):
    self.server = PythonHTTPServer(host, port)
    self.thread = Thread(target=self.server.serve_forever)

  def listen(self):
    self.thread.daemon = True
    self.thread.start()

  def shutdown(self):
    self.server.socket.close()

  def get_latest_request(self):
    try:
      incoming_request = requests.get(block=True, timeout=0.030)
    except Empty:
      return None

    request = Request()
    request.path = incoming_request['path']
    request.method = incoming_request['method']
    return request
