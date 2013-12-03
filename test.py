#!/usr/bin/python3
from debug import pprint, pprintxml, shell, profile, debug as sj_debug
import unittest
import unittest.mock
import gc
from db.database import CouchDBAdapter

import tulip
from tulip import test_utils
from config import config
import logging
import contextlib
import threading
from server import HttpServer as AppServer
import urllib.parse
from debug import set_except_hook
from nose.tools import nottest


class TestCase(unittest.TestCase):
    def setUp(self):
        set_except_hook()
        logging.getLogger('tulip').level = logging.ERROR
        self.loop = tulip.new_event_loop()
        tulip.set_event_loop(self.loop)

    def tearDown(self):
        # just in case if we have transport close callbacks
        test_utils.run_briefly(self.loop)

        self.loop.close()
        gc.collect()


class CouchDBTestCase(TestCase):
    database = 'tulipblog'

    def setUp(self):
        super(CouchDBTestCase, self).setUp()
        self.db = CouchDBAdapter(
            'http://%(username)s:%(password)s@localhost:5984/' %
            config['couchdb'], self.database)

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete_db())
        assert hasattr(r, 'ok') and r.ok is True, "db call failed: %s" % str(r)
        super(CouchDBTestCase, self).tearDown()

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
        thread_loop = tulip.new_event_loop()
        tulip.set_event_loop(thread_loop)

        socks = thread_loop.run_until_complete(
            thread_loop.start_serving(
                lambda: AppServer(router, keep_alive=0.5),
                host, port, ssl=sslcontext))

        waiter = tulip.Future()
        loop.call_soon_threadsafe(
            fut.set_result, (thread_loop, waiter, socks[0].getsockname()))

        thread_loop.run_until_complete(waiter)

        # close opened trnsports
        for tr in transports:
            tr.close()

        test_utils.run_briefly(thread_loop)  # call close callbacks

        for s in socks:
            thread_loop.stop_serving(s)

        thread_loop.stop()
        thread_loop.close()
        gc.collect()

    fut = tulip.Future()
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
    sj_debug() ###############################################################
    nose.run(argv=sys.argv+['-s'])