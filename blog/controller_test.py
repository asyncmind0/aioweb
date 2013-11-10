from blog.controller import HomeController
import unittest
import unittest.mock
import re

import tulip
from tulip.http import server
from tulip.http import errors
from tulip.test_utils import run_briefly

class ControllerTest (unittest.TestCase):
    def setUp(self):
        self.loop = tulip.new_event_loop()
        tulip.set_event_loop(self.loop)
        self.controller = HomeController()

    def tearDown(self):
        self.loop.close()
        
    def test_get_all(self):
        docs = self.controller.get_all()
        assert docs is not None










