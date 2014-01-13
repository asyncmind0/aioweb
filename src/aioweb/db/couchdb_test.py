import unittest
import asyncio
from aioweb.test import TestCase
from aioweb.db import CouchDBAdapter


class CouchDBAdapterTest(TestCase):
    database = 'asyncioblog'

    def setUp(self):
        super(CouchDBTestCase, self).setUp()
        self.db = CouchDBAdapter(
            'http://%(username)s:%(password)s@localhost:5984/' %
            self.config['couchdb'], self.config['couchdb']['database'])

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete_db())
        assert hasattr(r, 'ok') and r.ok is True, "db call failed: %s" % str(r)
        super(CouchDBTestCase, self).tearDown()
