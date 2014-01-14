import logging
from .model import Model
from .couchdb import CouchDBAdapter
try:
    from .mongodb import MongoDBAdapter
except ImportError:
    logging.exception("Pymongo is not installed ?")


def get_db(config=None):
    if not config:
        from aioweb.config import config
    return CouchDBAdapter(
        'http://%(username)s:%(password)s@localhost:5984/' %
        config['couchdb'], config['couchdb']['database'], )
