"""Simple server written using an event loop."""

import argparse
import email.message
import logging
import os
import sys
import inspect

import asyncio
from aiohttp import server
import aiohttp
import cgi
from errors import ErrorHandlerMixin


class HttpServer(server.ServerHttpProtocol):
    def __init__(self, router, *args, **kwargs):
        super(HttpServer, self).__init__(*args, **kwargs)
        self.router = router
        self.default_args = kwargs.get('default_args')
        self.logger = logging.getLogger(self.__class__.__name__)

    @asyncio.coroutine
    def handle_request(self, message, payload):
        response = None
        # logging.debug('method = {!r}; path = {!r}; version = {!r}'.format(
        #    message.method, message.path, message.version))
        handlers, request_args, handler_args = self.router.get_handler(message.path)
        if handlers:
            for handler in handlers:
                try:
                    handler = handler(**handler_args)
                    handler.initialize(self, message, payload,
                                                  prev_response=response)
                except Exception as e:
                    return self.handle_error(500, message, payload, exc=e)
                    # logging.exception(e)
                    # response = self.router.handle_error(e)
                else:
                    try:
                        response = handler(request_args=request_args)
                        if (inspect.isgenerator(response) or
                                isinstance(response, asyncio.Future)):
                            response = yield from response
                        if not isinstance(response, aiohttp.Response):
                            response = handler.response
                    except aiohttp.errors.HttpStatusException as e:
                        self.logger.debug("%s: %s", e.code, e.message)
                        return self.handle_error(e.code, message, payload, exc=e)
                    except Exception as e:
                        return self.handle_error(500, message, payload, exc=e)
                        # response = handler.handle_error(e, message,
                        # request_args=args)
            if not isinstance(response, aiohttp.Response):
                return self.handle_error(404, message, payload)
        else:
            return self.handle_error(404, message, payload)

        response.write_eof()
        if response.keep_alive():
            self.keep_alive(True)

    def log_access(self, status, message, *args, **kw):
        logging.debug("%s: %s", status, message.path if message else "")
