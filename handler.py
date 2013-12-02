from debug import pprint, pprintxml, shell, profile, debug as sj_debug
import tulip
import tulip.http
import email.message
from urllib.parse import urlparse
import cgi
from errors import ErrorHandlerMixin
import logging
import email.parser
import io
import urllib
import json
import http.cookies


class Handler(ErrorHandlerMixin):
    request = None

    def __init__(self, db=None, write_headers=True):
        self.response = None
        self.write_headers = write_headers
        self.db = db
        self.logger = logging.getLogger(self.__class__.__name__.lower())

    def initialize(self, server, message, payload, prev_response=None):
        self.server = server
        self.request = message
        self.body = yield from payload.read()
        self.headers = dict(self.request.headers)
        self._cookie = http.cookies.SimpleCookie(self.headers.get('COOKIE'))
        self.prev_response = prev_response
        if self.write_headers:
            self.response = self._write_headers()

    def __call__(self, request_args=None):
        self.response.write(b'base handler')
        return self.response

    def get_form_data(self, form=False):
        ct = self.headers.get('content-type', self.headers.get('CONTENT-TYPE', '')).lower()
        resp = {}

        # application/x-www-form-urlencoded
        if ct == 'application/x-www-form-urlencoded':
            resp['form'] = urllib.parse.parse_qs(self.body.decode('latin1'))

        # multipart/form-data
        elif ct.startswith('multipart/form-data'):  # pragma: no cover
            out = io.BytesIO()
            for key, val in self.headers.items():
                out.write(bytes('{}: {}\r\n'.format(key, val), 'latin1'))

            out.write(b'\r\n')
            out.write(self.body)
            out.write(b'\r\n')
            out.seek(0)

            message = email.parser.BytesParser().parse(out)
            if message.is_multipart():
                for msg in message.get_payload():
                    if msg.is_multipart():
                        logging.warn('multipart msg is not expected')
                    else:
                        key, params = cgi.parse_header(
                            msg.get('content-disposition', ''))
                        params['data'] = msg.get_payload()
                        params['content-type'] = msg.get_content_type()
                        resp['multipart-data'].append(params)

        return resp['form'] if form else resp 

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
        #response.send_headers()
        return response

    def render(self, *args, **data):
        self.response.send_headers()
        self.response.write(self.renderer.render(*args, **data))

    @property
    def cookies(self):
        return self._cookie

    @cookies.setter
    def cookies(self, cookies):
        _cookie = cookies
        if isinstance(cookies, dict):
            _cookies = http.cookies.SimpleCookie()
            for name, value in cookies.items():
                _cookies[name] = value
        else:
            assert isinstance(cookies, http.cookies.SimpleCookie), \
                "Cookies have to be http.cookies.SimpleCookie or dict"

        resp = self.response
        for cookie in _cookies.output(header='').split('\n'):
            resp.add_header('Set-Cookie', cookie.strip())
