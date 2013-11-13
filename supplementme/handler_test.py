from debug import pprint, shell, profile, debug as sj_debug
import unittest
import unittest.mock
from test import TestCase
from .handler import HomeHandler


class HomeHandlerTest(TestCase):
    def setUp(self):
        super(HomeHandlerTest, self).setUp()
        self.handler = HomeHandler()
        self.transport = unittest.mock.Mock()
        self.handler.response = self.transport

    def tearDown(self):
        super(HomeHandlerTest, self).tearDown()

    def test_home(self):
        r = self.handler()
        assert self.transport.write.called is True, "write Not called"
        assert len(self.transport.write.call_args[0][0]) > 0
        sj_debug() ###############################################################

