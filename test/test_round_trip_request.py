from mocks.app import App
from unittest import TestCase
from stenograpi import Stenograpi
from http.client import HTTPConnection

class TestProxy(TestCase):

    def setUp(self):
        self.app = App('localhost', port=0)
        self.app.listen()
        self.stenograpi = Stenograpi('localhost', port=0, app_port=self.app.port)
        self.stenograpi.listen()

    def tearDown(self):
        self.app.shutdown()
        self.stenograpi.shutdown()

    def test_GET_response_body_is_proxied_back_to_the_client(self):
        self.app.route('GET', '/', 200, b'GET RESPONSE')
        client = HTTPConnection('localhost', self.stenograpi.port)
        client.request('GET', '/')
        response = client.getresponse()
        self.assertEqual(response.read(), b'GET RESPONSE')

    def test_GET_response_header_is_proxied_back_to_the_client(self):
        self.app.route('GET', status=200, headers={'Foo': 'Bar'})
        client = HTTPConnection('localhost', self.stenograpi.port)
        client.request('GET', '/')
        response = client.getresponse()
        self.assertEqual(response.getheader('Foo'), 'Bar')

    def test_Server_response_header_is_empty_by_default(self):
        self.app.route('GET', status=200)
        client = HTTPConnection('localhost', self.stenograpi.port)
        client.request('GET', '/')
        response = client.getresponse()
        self.assertEqual(response.getheader('Server'), None)

    def test_POST_response_body_is_proxied_back_to_the_client(self):
        self.app.route('POST', '/', 200, b'POST RESPONSE')
        client = HTTPConnection('localhost', self.stenograpi.port)
        client.request('POST', '/')
        response = client.getresponse()
        self.assertEqual(response.read(), b'POST RESPONSE')

    def test_404_response_status_is_proxied_back_to_the_client(self):
        self.app.route('GET', '/not-found', 404, b'Not found')
        client = HTTPConnection('localhost', self.stenograpi.port)
        client.request('GET', '/not-found')
        response = client.getresponse()
        self.assertEqual(response.status, 404)
