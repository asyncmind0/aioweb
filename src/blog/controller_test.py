from .controller import HomeController
from .model import Post
from loremipsum import generate_sentence, generate_paragraph
from datetime import datetime
from aioweb.test import CouchDBTestCase


class ControllerTest(CouchDBTestCase):
    def setUp(self):
        super(ControllerTest, self).setUp()
        self.loop.run_until_complete(Post.sync_design(self.db))
        self.controller = HomeController(self.db)

    def tearDown(self):
        r = self.loop.run_until_complete(self.db.delete_db())
        self.assertEqual(r.ok, True)
        super(CouchDBTestCase, self).tearDown()

    def test_new_post(self):
        post = Post(date=str(datetime.now()),
                    body=generate_paragraph()[2],
                    title=generate_sentence()[2])
        r = self.loop.run_until_complete(self.controller.new_post(post))
        assert r is True
