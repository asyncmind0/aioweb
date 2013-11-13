import tulip
import tulip.http
import email.message
from urllib.parse import urlparse
import cgi


class Handler(object):
    request = None

    def __init__(self, db=None, write_headers=True):
        self.response = None
        self.write_headers = write_headers
        self.db = db

    def initialize(self, server, message, payload, prev_response=None):
        self.server = server
        self.request = message
        self.payload = payload
        self.prev_response = prev_response
        if self.write_headers:
            self.response = self._write_headers()

    def __call__(self, request_args=None):
        self.response.write(b'base handler')
        return self.response

    @property
    def query(self):
        if not self.request:
            return {}
        parsed = urlparse(self.request.path)
        querydict = cgi.parse_qs(parsed.query)
        for key, value in querydict.items():
            if isinstance(value, list) and len(value) < 2:
                querydict[key] = value[0] if value else None
        return querydict

    def _write_headers(self):
        headers = email.message.Message()
        response = tulip.http.Response(
            self.server.transport, 200, close=True)
        response.add_header('Transfer-Encoding', 'chunked')

        # content encoding
        accept_encoding = headers.get('accept-encoding', '').lower()
        if 'deflate' in accept_encoding:
            response.add_header('Content-Encoding', 'deflate')
            response.add_compression_filter('deflate')
        elif 'gzip' in accept_encoding:
            response.add_header('Content-Encoding', 'gzip')
            response.add_compression_filter('gzip')

        response.add_chunking_filter(1025)

        response.add_header('Content-type', 'text/html')
        response.send_headers()
        return response

    def render(self, template, **data):
        self.response.write(self.renderer.render('home', **data))

    def handle_error(self, exception, request_args=None):
        """Default handler exception handler"""
        if not self.response:
            self.response = self._write_headers()

        self.response.write(("Error: %s" % str(exception)).encode('utf-8'))
