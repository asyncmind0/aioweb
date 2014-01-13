import logging
import asyncio
from .database import DatabaseAdapter
from pymongo.mongo_client import MongoClient

def _run_in_executor(method):
    def run(self, *args):
        loop = asyncio.get_event_loop()
        res = yield from loop.run_in_executor(None, method, self, *args)
        return res
    return run

class MongoDBAdapter(DatabaseAdapter):
    def __init__(self, url, dbname):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = MongoClient()
        self.db = getattr(self.client, dbname)


    @_run_in_executor
    def info(self):
        return self.client.server_info()

    @_run_in_executor
    def put(self, document, doc_id=None, **options):
        collection = document.data['doc_type']
        collection = getattr(self.db, collection)
        if '_id' in document.data and document.data['_id']:
            _id = collection.update(document.data)
        else:
            if '_id' in document.data:
                del document.data['_id']
            _id = collection.insert(document.data)
        document.data['_id'] = _id
        return document

