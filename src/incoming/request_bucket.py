from incoming import Request
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
