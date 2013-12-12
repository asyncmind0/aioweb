from debug import pprint, pprintxml, shell, profile, debug as sj_debug
import os
import sys
import json

import tulip
from tulip import streams
from tulip import protocols

from subprocess import Popen, PIPE
from test import TestCase, run_test_server, CouchDBTestCase
from . import get_routes
from .model import Nutrient, Meal
from auth import User
from static_handler import get_routes as get_static_routes
from .importer import import_sr25_nutr_def

def connect_write_pipe(file):
    loop = tulip.get_event_loop()
    protocol = protocols.Protocol()
    return loop._make_write_pipe_transport(file, protocol)

#
# Wrap a readable pipe in a stream
#


def connect_read_pipe(file):
    loop = tulip.get_event_loop()
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


class FunctionalTests(CouchDBTestCase):
    def setUp(self):
        super(FunctionalTests, self).setUp()
        self.loop.run_until_complete(User.sync_design(self.db))
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.loop.run_until_complete(Meal.sync_design(self.db))
        import_sr25_nutr_def(self.db, self.loop)
    def _run_phantom(self, url):
        # start subprocess and wrap stdin, stdout, stderr
        output = []
        phantom_cmd = "phantomjs static/run-jasmine.js %s" % url
        print(phantom_cmd)
        p = Popen(phantom_cmd.split(),
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        stdout = connect_read_pipe(p.stdout)
        stderr = connect_read_pipe(p.stderr)

        # interact with subprocess
        name = {stdout: 'OUT', stderr: 'ERR'}
        registered = {tulip.Task(stderr.readline()): stderr,
                      tulip.Task(stdout.readline()): stdout}
        timeout = None
        res = None
        while registered:
            done, pending = yield from tulip.wait(
                registered, timeout=timeout, return_when=tulip.FIRST_COMPLETED)
            if not done:
                break
            for f in done:
                stream = registered.pop(f)
                res = f.result()
                output.append(res.decode('utf8').rstrip())
                if res != b'':
                    registered[tulip.Task(stream.readline())] = stream
            timeout = 5.0
        return output

    def test_main_page(self):
        import logging
        logging.basicConfig(level=logging.DEBUG)
        router = get_static_routes()
        router.add_handler('/', get_routes(db=self.db))
        with run_test_server(self.loop, router=router, port=9999) as httpd:
            url = httpd.url("/")
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

    def test_main_page_ghost(self):
        from ghost import Ghost
        import logging
        logging.basicConfig(level=logging.DEBUG)
        router = get_static_routes()
        router.add_handler('/', get_routes(db=self.db))
        with run_test_server(self.loop, router=router, port=9999) as httpd:
            url = httpd.url("/")
            print(url)
            meth = 'get'
            ghost = Ghost()
            page, extra_resources = ghost.open(url)
            sj_debug() ###############################################################
            assert page.http_status == 200 
