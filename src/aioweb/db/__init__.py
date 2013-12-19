from .database import CouchDBAdapter


def get_db():
    from config import config
    return CouchDBAdapter(
        'http://%(username)s:%(password)s@localhost:5984/' %
        config['couchdb'], config['couchdb']['database'], )
