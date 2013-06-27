"""Simple server written using an event loop."""

import argparse
import email.message
import logging
import os
import sys
try:
    import ssl
except ImportError:  # pragma: no cover
    ssl = None

assert sys.version >= '3.3', 'Please use Python 3.3 or higher.'

import tulip
import tulip.http
from urllib.parse import urlparse

class HttpServer(tulip.http.ServerHttpProtocol):
    def __init__(self, router):
        self.router = router

    def handle_url(self, message, payload):
        return handler

    @tulip.coroutine
    def handle_request(self, message, payload):
        response = None
        print("MESSAGE")
        print('method = {!r}; path = {!r}; version = {!r}'.format(
            message.method, message.path, message.version))

        handlers, args = self.router.get_handler(message.path)
        if handlers:
            try:
                for handler in handlers:
                    response = handler(
                        self, message, payload, 
                        request_args=args,
                        prev_response=response)
            except Exception as e:
                response = tulip.http.Response(self.transport, 500, close=True)
                response.add_header('Content-type', 'text/html')
                response.send_headers()
                response.write(bytearray(str(e), "utf-8"))
        else:
            response = tulip.http.Response(server.transport, 404)

        response.write_eof()
        if response.keep_alive():
            self.keep_alive(True)


