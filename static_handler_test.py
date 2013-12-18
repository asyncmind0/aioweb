import unittest
import unittest.mock
from test import TestCase, run_test_server
from router import Router
from aiohttp import client
from static_handler import StaticFileHandler


class StaticFileHandlerTest(TestCase):
    def setUp(self):
        super(StaticFileHandlerTest, self).setUp()
        self.transport = unittest.mock.Mock()
        self.handler = StaticFileHandler("static", baseurl="/static/")
        self.handler.response = self.transport

    def test_static_file(self):
        router = Router()
        router.add_handler("/static/(.*)$", self.handler)
        with run_test_server(self.loop, router=router) as httpd:
            url = httpd.url('static', 'test.js')
            meth = 'get'
            r = self.loop.run_until_complete(
                client.request(meth, url))
            content1 = self.loop.run_until_complete(r.read())
            content = content1.decode()

            self.assertEqual(r.status, 200)
            self.cookies = r.cookies
            r.close()