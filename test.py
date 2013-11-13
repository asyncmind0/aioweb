import unittest
import unittest.mock
import gc
from db.database import CouchDBAdapter

import tulip
from tulip import test_utils
from config import config


class TestCase(unittest.TestCase):
    def setUp(self):
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
        self.assertEqual(r.ok, True)
        super(CouchDBTestCase, self).tearDown()
