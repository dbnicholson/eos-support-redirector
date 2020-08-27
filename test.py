#!/usr/bin/env python3

from collections import OrderedDict
import wsgiref.util
import unittest
from urllib.parse import urljoin

import redirector


class TestRedirector(unittest.TestCase):
    """Test support URL redirector"""

    # Paths that are mapped successfully
    mapped_paths = OrderedDict((
        ('/hc/en-us/articles/360041130271-What-is-a-pathway-',
         '/help-center/What-is-a-pathway'),
        ('/hc/en-us/articles/360041130271',
         '/help-center/What-is-a-pathway'),
        ('/hc/articles/360041130271',
         '/help-center/What-is-a-pathway'),
        ('/hc/pt/articles/360041130271/',
         '/help-center/What-is-a-pathway'),
    ))

    # Paths that are not mapped and fallback to an empty path
    fallback_paths = (
        '',
        '/',
        '/fake-url',
        '/hc/articles/12345'
        '/hc/en-us/articles/12345'
    )

    # Dictionary of test path to expected response
    TEST_PATHS = OrderedDict()
    for inpath, outpath in mapped_paths.items():
        TEST_PATHS[inpath] = {
            'path': outpath,
            'status': '301 Moved Permanently',
            'headers': [
                ('Location', urljoin(redirector.SUPPORT_URL, outpath)),
            ],
            'body': tuple(),
        }
    for path in fallback_paths:
        TEST_PATHS[path] = {
            'path': '',
            'status': '301 Moved Permanently',
            'headers': [
                ('Location', urljoin(redirector.SUPPORT_URL, '')),
            ],
            'body': tuple(),
        }

    def test_convert_path(self):
        """Test the convert_path() function"""
        for path, expected in self.TEST_PATHS.items():
            result = redirector.convert_path(path)
            self.assertEqual(result, expected['path'])

    class ResponseInfo:
        """Support class to store WSGI start_response() arguments"""
        def __init__(self):
            self.status = None
            self.headers = None

        def start_response(self, status, headers):
            self.status = status
            self.headers = headers

    def test_application(self):
        """Test the WSGI application() function"""
        for path, expected in self.TEST_PATHS.items():
            environ = {
                'PATH_INFO': path,
            }
            wsgiref.util.setup_testing_defaults(environ)
            info = self.ResponseInfo()
            body = redirector.application(environ, info.start_response)
            self.assertEqual(info.status, expected['status'])
            self.assertEqual(info.headers, expected['headers'])
            self.assertEqual(body, expected['body'])


if __name__ == '__main__':
    unittest.main()
