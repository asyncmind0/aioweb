import unittest
import unittest.mock
import re
import gc

import tulip
from tulip.http import server
from tulip.http import errors
from tulip.test_utils import run_briefly
from tulip import test_utils

from .database import CouchDBAdapter


class CouchDBAdapterTest(unittest.TestCase):
    def setUp(self):
        self.loop = tulip.new_event_loop()
        tulip.set_event_loop(self.loop)
        self.db = CouchDBAdapter(
            'http://xXxXxXxXxXx:xXxXxXxXxXx@localhost:5984/', 
            dbname='couchtest')
        r = self.loop.run_until_complete(self.db.create_db())
        self.test_document = {'test':'testdata'}
        r = self.loop.run_until_complete(self.db.put(self.test_document))
        assert r.ok == True
        self.test_document['id'] = r.id

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete(self.test_document['id']))
        assert r.ok == True
        r = self.loop.run_until_complete(self.db.delete_db())
        self.assertEqual(r.ok, True)
        # just in case if we have transport close callbacks
        test_utils.run_briefly(self.loop)

        self.loop.close()
        gc.collect()
        
    def test_info(self):
        with test_utils.run_test_server(self.loop) as httpd:
            r = self.loop.run_until_complete(self.db.info())
            self.assertEqual(r.db_name, self.db._dbname)

    def test_put(self):
        with test_utils.run_test_server(self.loop) as httpd:
            document = {'test':'testdata'}
            r = self.loop.run_until_complete(self.db.put(document))
            self.assertEqual(r.ok, True)

    def test_all(self):
        with test_utils.run_test_server(self.loop) as httpd:
            r = self.loop.run_until_complete(self.db.all())
            assert r.total_rows > 0

    def test_get(self):
        with test_utils.run_test_server(self.loop) as httpd:
            r = self.loop.run_until_complete(self.db.all())
            assert r.total_rows > 0
            one = r.rows[0]
            r = self.loop.run_until_complete(self.db.get(one['id']))
            assert r._id == one['id']

    def test_delete(self):
        with test_utils.run_test_server(self.loop) as httpd:
            document = {'test':'testdelete'}
            document = self.loop.run_until_complete(self.db.put(document))
            r = self.loop.run_until_complete(self.db.delete(document.id))
            assert r.ok == True
            r = self.loop.run_until_complete(self.db.get(document.id))
            assert r.reason == 'deleted'

    def test_view(self):
        with test_utils.run_test_server(self.loop) as httpd: