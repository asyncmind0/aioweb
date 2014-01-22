import os
import sys
import json

import asyncio
from asyncio import streams
from asyncio import protocols

from subprocess import Popen, PIPE
from .test import TestCase
from aioweb.test import run_test_server
from aioweb.db.couchdb_test import CouchDBTestCase
from .routes import get_routes
from .model import Nutrient, Meal
from aioweb.auth import User
from .importer import import_sr25_nutr_def
from nose.tools import nottest as broken

def connect_write_pipe(file):
    loop = asyncio.get_event_loop()
    protocol = protocols.Protocol()
    return loop._make_write_pipe_transport(file, protocol)

#
# Wrap a readable pipe in a stream
#


def connect_read_pipe(file):
    loop = asyncio.get_event_loop()
    stream_reader = streams.StreamReader()
    protocol = _StreamReaderProtocol(stream_reader)
    transport = loop._make_read_pipe_transport(file, protocol)
    return stream_reader


class _StreamReaderProtocol(protocols.Protocol):
    def __init__(self, stream_reader):
        self.stream_reader = stream_reader

    def connection_lost(self, exc):
        self.stream_reader.set_exception(exc)

    def data_received(self, data):
        self.stream_reader.feed_data(data)

    def eof_received(self):
        self.stream_reader.feed_eof()


class FunctionalTest(CouchDBTestCase):
    base_path = os.path.dirname(__file__)
    def setUp(self):
        super(FunctionalTest, self).setUp()
        import_sr25_nutr_def(self.db)

    def _run_phantom(self, url):
        # start subprocess and wrap stdin, stdout, stderr
        output = []
        phantom_cmd = ("phantomjs %s/run-jasmine.js %s" 
                       % (self.config['default']['staticroot'], url))
        print(phantom_cmd)
        p = Popen(phantom_cmd.split(),
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout = connect_read_pipe(p.stdout)
        stderr = connect_read_pipe(p.stderr)

        # interact with subprocess
        name = {stdout: 'OUT', stderr: 'ERR'}
        registered = {asyncio.Task(stderr.readline()): stderr,
                      asyncio.Task(stdout.readline()): stdout}
        timeout = None
        res = None
        while registered:
            done, pending = yield from asyncio.wait(
                registered, timeout=timeout, return_when=asyncio.FIRST_COMPLETED)
            if not done:
                break
            for f in done:
                stream = registered.pop(f)
                res = f.result()
                output.append(res.decode('utf8').rstrip())
                if res != b'':
                    registered[asyncio.Task(stream.readline())] = stream
            timeout = 5.0
        return output
        
    def _test_page(self, url):
        router = get_routes()
        with run_test_server(self.loop, router=router, port=9999) as httpd:
            url = httpd.url(url)
            print(url)
            meth = 'get'
            r = self.loop.run_until_complete(
                self._run_phantom(url))
            spec = []
            startspec = False
            for line in r:
                if line.startswith('ENDSPEC'):
                    break
                if startspec:
                    spec.append(line)
                if line.startswith('STARTSPEC'):
                    startspec = True
            spec = json.loads("".join(spec))
            for sp in spec:
                print(sp['description'])
                print("\t"+sp['status'])


class MainPageFunctionalTests(FunctionalTest):

    def test_main_page(self):
        self._test_page("/")

    @broken
    def test_main_page_ghost(self):
        from ghost import Ghost
        import logging
        logging.basicConfig(level=logging.DEBUG)
        router = get_static_routes()
        router.add_handler('/', get_routes())
        with run_test_server(self.loop, router=router, port=9999) as httpd:
            url = httpd.url("/")
            print(url)
            meth = 'get'
            ghost = Ghost()
            page, extra_resources = ghost.open(url)
            assert page.http_status == 200 
