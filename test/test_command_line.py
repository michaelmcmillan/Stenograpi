from unittest.mock import patch
from unittest import TestCase
from main import parse_args
from io import StringIO


class TestCommandLine(TestCase):

    @patch('sys.stderr', new_callable=StringIO)
    def test_exception_is_raised_if_missing_hostname(self, stderr):
        with self.assertRaises(BaseException):
            parse_args([])
        self.assertIn('required: hostname', stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_exception_is_raised_if_missing_port(self, stderr):
        with self.assertRaises(BaseException):
            parse_args(['localhost'])
        self.assertIn('required: port', stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_exception_is_raised_if_missing_app_hostname(self, stderr):
        with self.assertRaises(BaseException):
            parse_args(['localhost', '1337'])
        self.assertIn('required: app-hostname', stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_exception_is_raised_if_missing_app_port(self, stderr):
        with self.assertRaises(BaseException):
            parse_args(['localhost', '1337', 'localhost'])
        self.assertIn('required: app-port', stderr.getvalue())

    @patch('sys.stderr', new_callable=StringIO)
    def test_exception_is_not_raised_if_all_required_flags_are_provided(self, stderr):
        arguments = parse_args(['localhost', '1337', 'localhost', '1338'])
        self.assertEqual(arguments.hostname, 'localhost')
        self.assertEqual(arguments.port, 1337)
        self.assertEqual(getattr(arguments, 'app-port'), 1338)
        self.assertEqual(getattr(arguments, 'app-hostname'), 'localhost')
