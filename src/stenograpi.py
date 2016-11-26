from queue import Empty
from threading import Thread
from incoming import Request, requests, PythonHTTPServer

class Stenograpi:

    def __init__(self, host, port, app_port):
        self.server = PythonHTTPServer(host, port, app_port)
        self.thread = Thread(target=self.server.serve_forever)

    def listen(self):
        self.thread.daemon = True
        self.thread.start()

    @property
    def port(self):
        return self.server.socket.getsockname()[1]

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
