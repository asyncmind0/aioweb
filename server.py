from debug import pprint, shell, profile, debug as sj_debug
"""Simple server written using an event loop."""

import argparse
import email.message
import logging
import os
import sys


import tulip
import tulip.http
import cgi

class HttpServer(tulip.http.ServerHttpProtocol):
    def __init__(self, router, *args, **kwargs):
        super(HttpServer, self).__init__(*args, **kwargs)
        self.router = router

    @tulip.coroutine
    def handle_request(self, message, payload):
        response = None
        logging.debug('method = {!r}; path = {!r}; version = {!r}'.format(
            message.method, message.path, message.version))
        handlers, args = self.router.get_handler(message.path)
        if handlers:
            for handler in handlers:
                try:
                    logging.debug("handler: %s", handler)
                    handler.initialize(self, message, payload, prev_response=response)
                except Exception as e:
                    response = self.router.handle_error(e)
                else:
                    try:
                        result = handler(request_args=args)
                        response = handler.response
                    except Exception as e:
                        response = handler.handle_error(e, request_args=args)
            if not response:
                raise tulip.http.HttpStatusException(404, message="No Handler found")
        else:
            raise tulip.http.HttpStatusException(404)

        response.write_eof()
        if response.keep_alive():
            self.keep_alive(True)
            
    


