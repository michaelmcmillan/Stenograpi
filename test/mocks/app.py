from http import server, HTTPStatus
from threading import Thread
from socketserver import ThreadingMixIn

class AppHandler(server.BaseHTTPRequestHandler):

    def do_ALL(self):
        App.routes[(self.command, self.path)](self)

    def send_error(self, code, message=None, explain=None):
        if code == HTTPStatus.NOT_IMPLEMENTED:
            self.do_ALL()
        else:
            return super().send_error(code, message, explain)

    def log_message(self, *args, **kwargs):
        return

    def send_header(self, *args, **kwargs):
        key, value = args
        if key == 'Server' and 'BaseHTTP' in value:
            return
        super().send_header(*args, **kwargs)

class AppHTTPServer(ThreadingMixIn, server.HTTPServer):
    pass

class App:

    routes = {}

    def __init__(self, host, port):
        self.server = AppHTTPServer((host, port), AppHandler)
        self.thread = Thread(target=self.server.serve_forever)

    def listen(self):
        self.thread.daemon = True
        self.thread.start()

    @property
    def port(self):
        return self.server.socket.getsockname()[1]

    def route(self, method='GET', path='/', status=200, body=b'', headers=None):
        def response_func(request):
            request.send_response(status)
            if headers:
                for key, value in headers.items():
                    request.send_header(key, value)
            request.end_headers()
            request.wfile.write(body)
        App.routes[(method, path)] = response_func

    def shutdown(self):
        self.server.socket.close()
