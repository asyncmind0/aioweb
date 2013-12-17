from config import config
from .database import CouchDBAdapter


def get_db():
    return CouchDBAdapter(
        'http://%(username)s:%(password)s@localhost:5984/' %
        config['couchdb'], 'nutrition', )
