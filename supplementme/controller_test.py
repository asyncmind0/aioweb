from .controller import NutrientsController
import unittest
import unittest.mock
import re

import tulip
from tulip.http import server
from tulip.http import errors
from tulip.test_utils import run_briefly
from db.database import CouchDBAdapter
from loremipsum import generate_sentence, generate_paragraph
from datetime import datetime
from .model import Nutrient, Food
from config import config

class ControllerTest (unittest.TestCase):
    def setUp(self):
        self.loop = tulip.new_event_loop()
        tulip.set_event_loop(self.loop)
        self.db = CouchDBAdapter(
            'http://%(username)s:%(password)s@localhost:5984/' % config['couchdb'], 'supplementme_test', )
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.controller = NutrientsController(self.db)

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete_db())
        self.assertEqual(r.ok, True)
        # just in case if we have transport close callbacks
        run_briefly(self.loop)
        self.loop.close()

    def test_new(self, name='vitamin_c'):
        post = Nutrient(quantity=10, name=name)
        r = self.loop.run_until_complete(self.controller.new(post))
        assert r.ok is True, str(r)

    def test_all(self):
        self.test_new()
        r = self.loop.run_until_complete(Nutrient.all(self.db))
        assert len(r.rows) > 0, str(r)

    def test_keys(self):
        test_names = ['vitamin_d', 'vitamin_c']
        self.test_new(test_names[0])
        self.test_new(test_names[0])
        self.test_new(test_names[0])
        self.test_new()
        self.test_new()
        r = self.loop.run_until_complete(self.controller.keys())
        assert len(r) > 0, str(r)
        self.assertListEqual(sorted(r), sorted(test_names)), str(r)

