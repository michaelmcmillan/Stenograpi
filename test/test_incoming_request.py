from unittest import TestCase
from stenograpi import Stenograpi
from http.client import HTTPConnection

class TestHTTPServerRequest(TestCase):

    def setUp(self):
        self.server = Stenograpi('localhost', port=0, app_port=0)
        self.server.listen()

    def tearDown(self):
        self.server.shutdown()

    def test_request_method_is_GET_if_GET_request_was_sent(self):
        client = HTTPConnection('localhost', self.server.port)
        client.request('GET', '/')
        received_request = self.server.get_latest_request()
        self.assertEqual(received_request.method, 'GET')

    def test_request_method_is_POST_if_POST_request_was_sent(self):
        client = HTTPConnection('localhost', self.server.port)
        client.request('POST', '/')
        received_request = self.server.get_latest_request()
        self.assertEqual(received_request.method, 'POST')

    def test_request_method_is_BATMAN_if_BATMAN_request_was_sent(self):
        client = HTTPConnection('localhost', self.server.port)
        client.request('BATMAN', '/')
        received_request = self.server.get_latest_request()
        self.assertEqual(received_request.method, 'BATMAN')

    def test_request_path_is_index_if_index_was_sent(self):
        client = HTTPConnection('localhost', self.server.port)
        client.request('GET', '/index')
        received_request = self.server.get_latest_request()
        self.assertEqual(received_request.path, '/index')

    def test_request_path_is_root_if_root_was_sent(self):
        client = HTTPConnection('localhost', self.server.port)
        client.request('GET', '/')
        received_request = self.server.get_latest_request()
        self.assertEqual(received_request.path, '/')

    def test_second_request_is_returned_when_latest_called_twice(self):
        first_client = HTTPConnection('localhost', self.server.port)
        first_client.request('GET', '/foo')
        second_client = HTTPConnection('localhost', self.server.port)
        second_client.request('GET', '/bar')
        self.server.get_latest_request()
        second_received_request = self.server.get_latest_request()
        self.assertEqual(second_received_request.path, '/bar')

    def xtest_none_is_returned_when_there_are_no_requests(self):
        received_request = self.server.get_latest_request()
        self.assertEqual(received_request, None)
