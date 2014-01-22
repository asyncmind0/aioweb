import unittest
import asyncio
from aioweb.test import TestCase, TestModel, run_briefly
from aioweb.db import get_db
from aioweb.db.couchdb import CouchDBAdapter


class CouchDBAdapterTest(TestCase):
    database = 'asyncioblog'

    def setUp(self):
        super(CouchDBAdapterTest, self).setUp()
        self.db = CouchDBAdapter(
            'http://%(username)s:%(password)s@localhost:5984/' %
            self.config['couchdb'], self.config['couchdb']['database'])
        self.loop.run_until_complete(self.db.sync_designs(force=True))
        run_briefly(self.loop)

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete_db())
        assert hasattr(r, 'ok') and r.ok is True, "db call failed: %s" % str(r)
        super(CouchDBAdapterTest, self).tearDown()

    def test_put(self):
        testdata = TestModel(name="testmodel")
        r = self.loop.run_until_complete(self.db.put(testdata))
        assert hasattr(r, 'ok') and r.ok is True, "db call failed: %s" % str(r)
        return r.id

    def test_get(self):
        _id = self.test_put()
        r = self.loop.run_until_complete(self.db.get(_id))
        assert r.get('_id') == _id, "db call failed: %s" % str(r)


class CouchDBTestCase(TestCase):
    def setUp(self):
        super(CouchDBTestCase, self).setUp()
        self.db = get_db(self.config)
        self.loop.run_until_complete(self.db.sync_designs(force=True))

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete_db())
        assert hasattr(r, 'ok') and r.ok is True, "db call failed: %s" % str(r)
        super(CouchDBTestCase, self).tearDown()

