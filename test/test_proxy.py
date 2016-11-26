from app import App
from unittest import TestCase
from server import StenograpiServer
from http.client import HTTPConnection

class TestProxy(TestCase):

    def setUp(self):
        self.app = App('localhost', 1338)
        self.app.listen()
        self.server = StenograpiServer('localhost', 1337)
        self.server.listen()

    def tearDown(self):
        self.app.shutdown()
        self.server.shutdown()

    def test_GET_response_body_is_proxied_to_the_app_under_test(self):
        self.app.route('GET', '/', 200, b'GET RESPONSE')
        client = HTTPConnection('localhost', 1337)
        client.request('GET', '/')
        response = client.getresponse()
        self.assertEqual(response.read(), b'GET RESPONSE')

    def test_POST_response_body_is_proxied_to_the_app_under_test(self):
        self.app.route('POST', '/', 200, b'POST RESPONSE')
        client = HTTPConnection('localhost', 1337)
        client.request('POST', '/')
        response = client.getresponse()
        self.assertEqual(response.read(), b'POST RESPONSE')

    def test_404_response_status_is_proxied_to_the_app_under_test(self):
        self.app.route('GET', '/not-found', 404, b'Not found')
        client = HTTPConnection('localhost', 1337)
        client.request('GET', '/not-found')
        response = client.getresponse()
        self.assertEqual(response.status, 404)
