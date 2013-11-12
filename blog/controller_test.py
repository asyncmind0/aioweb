from .controller import HomeController
import unittest
import unittest.mock
import re

import tulip
from tulip.http import server
from tulip.http import errors
from tulip.test_utils import run_briefly
from .model import Post
from db.database import CouchDBAdapter
from loremipsum import generate_sentence, generate_paragraph
from datetime import datetime
from .model import Post
from config import config

class ControllerTest (unittest.TestCase):
    def setUp(self):
        self.loop = tulip.new_event_loop()
        tulip.set_event_loop(self.loop)
        self.db = CouchDBAdapter(
            'http://%(username)s:%(password)s@localhost:5984/' % config['couchdb'], 'tulipblog', )
        self.loop.run_until_complete(Post.sync_design(self.db))
        self.controller = HomeController(self.db)

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete_db())
        self.assertEqual(r.ok, True)
        # just in case if we have transport close callbacks
        run_briefly(self.loop)
        self.loop.close()

    def test_all(self):
        r = self.loop.run_until_complete(HomeController.all(self.db))
        assert len(r.rows) > 0

    def test_new_post(self):
        post = Post(date=str(datetime.now()),
                    body=generate_paragraph()[2],
                    title=generate_sentence()[2])
        r = self.loop.run_until_complete(self.controller.new_post(post))
        assert r is True










