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
