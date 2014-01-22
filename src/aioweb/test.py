#!/usr/bin/python3
import unittest
import unittest.mock
import gc
import os
from aioweb.db import CouchDBAdapter, Model, get_db

import asyncio
from aiohttp import test_utils
import logging
import contextlib
import threading
from aioweb.server import HttpServer as AppServer
import urllib.parse
from debug import set_except_hook
from nose.tools import nottest
from aioweb.util import deep_update
from aioweb.config import configure_logging


def run_briefly(loop):
    @asyncio.coroutine
    def once():
        pass
    t = asyncio.Task(once(), loop=loop)
    loop.run_until_complete(t)


def test_logging(config):
    deep_update(config, {
        'version': 1,
        'disable_existing_loggers': False,
        'incremental': True,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'},
        },
        'loggers': {
            'config': {
                'handlers': ['console'],
                'level': 'WARN',
                'propagate': False
            },
            'CouchDBAdapter': {
                'handlers': ['console'],
                'level': 'WARN',
                'propagate': False
            },
        }
    })
    logging.config.dictConfig(config)


class TestCase(unittest.TestCase):
    config_name = "testing"
    base_path = os.path.dirname(__file__)

    def setUp(self):
        set_except_hook()
        from aioweb.config import set_config
        self.config = set_config(self.base_path, self.config_name)
        loggingconfig = configure_logging(self.base_path)
        test_logging(loggingconfig)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        # just in case if we have transport close callbacks
        test_utils.run_briefly(self.loop)
        self.loop.close()
        gc.collect()


class TestModel(Model):
    required_fields = ['name']
    pass


@nottest
@contextlib.contextmanager
def run_test_server(loop, *, host='127.0.0.1', port=0,
                    use_ssl=False, router=None):
    properties = {}
    transports = []

    class HttpServer:

        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.address = (host, port)
            self._url = '{}://{}:{}'.format(
                'https' if use_ssl else 'http', host, port)

        def __getitem__(self, key):
            return properties[key]

        def __setitem__(self, key, value):
            properties[key] = value

        def url(self, *suffix):
            return urllib.parse.urljoin(
                self._url, '/'.join(str(s) for s in suffix))

    if use_ssl:
        here = os.path.join(os.path.dirname(__file__), '..', 'tests')
        keyfile = os.path.join(here, 'sample.key')
        certfile = os.path.join(here, 'sample.crt')
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslcontext.load_cert_chain(certfile, keyfile)
    else:
        sslcontext = None

    def run(loop, fut):
        thread_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(thread_loop)

        server = thread_loop.run_until_complete(
            thread_loop.create_server(
                lambda: AppServer(router, keep_alive=0.5),
                host, port, ssl=sslcontext))
        socks = server.sockets

        waiter = asyncio.Future()
        loop.call_soon_threadsafe(
            fut.set_result, (thread_loop, waiter, socks[0].getsockname()))

        try:
            thread_loop.run_until_complete(waiter)
        finally:
            # call pending connection_made if present
            run_briefly(thread_loop)

            # close opened trnsports
            for tr in transports:
                tr.close()

            run_briefly(thread_loop)  # call close callbacks

            server.close()
            thread_loop.stop()
            thread_loop.close()
            gc.collect()

    fut = asyncio.Future()
    server_thread = threading.Thread(target=run, args=(loop, fut))
    server_thread.start()

    thread_loop, waiter, addr = loop.run_until_complete(fut)
    try:
        yield HttpServer(*addr)
    finally:
        thread_loop.call_soon_threadsafe(waiter.set_result, None)
        server_thread.join()


def __main__():
    import nose
    nose.run(argv=sys.argv+['-s'])
