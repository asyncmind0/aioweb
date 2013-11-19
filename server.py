from debug import pprint, shell, profile, debug as sj_debug
"""Simple server written using an event loop."""

import argparse
import email.message
import logging
import os
import sys
import inspect

import tulip
import tulip.http
import cgi
from errors import ErrorHandlerMixin


class HttpServer(tulip.http.ServerHttpProtocol):
    def __init__(self, router, *args, **kwargs):
        super(HttpServer, self).__init__(*args, **kwargs)
        self.router = router
        self.default_args = kwargs.get('default_args')

    @tulip.coroutine
    def handle_request(self, message, payload):
        response = None
        logging.debug('method = {!r}; path = {!r}; version = {!r}'.format(
            message.method, message.path, message.version))
        handlers, args = self.router.get_handler(message.path)
        if handlers:
            for handler in handlers:
                try:
                    handler.initialize(self, message, payload,
                                       prev_response=response)
                except Exception as e:
                    return self.handle_error(500, message, payload, exc=e)
                    #logging.exception(e)
                    #response = self.router.handle_error(e)
                else:
                    try:
                        response = handler(request_args=args)
                        if (inspect.isgenerator(response) or
                            isinstance(response, tulip.Future)):
                            response = yield from response
                        if not isinstance(response, tulip.http.Response):
                            response = handler.response
                    except Exception as e:
                        return self.handle_error(500, message, payload, exc=e)
                        #response = handler.handle_error(e, message, request_args=args)
            if not isinstance(response, tulip.http.Response):
                return self.handle_error(404, message, payload)
        else:
            return self.handle_error(404, message, payload)

        response.write_eof()
        if response.keep_alive():
            self.keep_alive(True)

    def log_access(self, status, message, *args, **kw):
        logging.debug("%s: %s", status, message.path)