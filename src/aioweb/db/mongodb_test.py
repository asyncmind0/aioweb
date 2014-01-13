import unittest
import asyncio
from aioweb.test import TestCase
from aioweb.db import MongoDBAdapter
from aioweb.db.model import Model
from pymongo.mongo_client import MongoClient


class TestModel(Model):
    required_fields = ['name']
    pass


class MongoDBAdapterTest(TestCase):
    def setUp(self):
        super(MongoDBAdapterTest, self).setUp()
        self.db = MongoDBAdapter('', 'testdb')

    def test_server_info(self):
        resp = self.loop.run_until_complete(self.db.info())
        assert 'version' in resp

    def test_put(self):
        data = TestModel(name='test')
        resp = self.loop.run_until_complete(self.db.put(data))
        assert hasattr(resp, '_id'), resp.__dict__

    def test_mongo(self):
        client = MongoClient()
        db = client.test_database
        collection = db.test_collection
        import datetime
        post = {"author": "Mike",
                "text": "My first blog post!",
                "tags": ["mongodb", "python", "pymongo"],
                "date": datetime.datetime.utcnow()}
        posts = db.posts
        post_id = posts.insert(post)
        print(post_id)
        print(client.server_info())
