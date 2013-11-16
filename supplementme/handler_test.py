import unittest
import unittest.mock
from test import CouchDBTestCase
from test import TestCase
from .handler import HomeHandler, AddFoodHandler


class HomeHandlerTest(CouchDBTestCase):
    def setUp(self):
        super(HomeHandlerTest, self).setUp()
        self.handler = HomeHandler(self.db)
        self.transport = unittest.mock.Mock()
        self.handler.response = self.transport

    def tearDown(self):
        super(HomeHandlerTest, self).tearDown()

    def test_home(self):
        r = self.loop.run_until_complete(self.handler())
        assert self.transport.write.called is True, "write Not called"
        assert len(self.transport.write.call_args[0][0]) > 0
        
class AddFoodHandlerTest(TestCase):
    def setUp(self):
        super(AddFoodHandlerTest, self).setUp()
        self.handler = AddFoodHandler()
        self.transport = unittest.mock.Mock()
        self.handler.response = self.transport

    def test_add_food(self):
        r = self.loop.run_until_complete(self.handler())
        assert self.transport.write.called is True, "write Not called"
        assert len(self.transport.write.call_args[0][0]) > 0

