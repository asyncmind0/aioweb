from db.database import CouchDBAdapter
from datetime import datetime


class BaseController(object):
    def __init__(self, *args, **kwargs):
        self.db = CouchDBAdapter('tulipblog', 'http://xXxXxXxXxXx:xXxXxXxXxXx@localhost:5984/')


class HomeController(BaseController):
    def __init__(self, *args, **kwargs):
        super(HomeController, self).__init__(*args, **kwargs)

    def store_query(self, query):
        query['datetime'] = datetime.now()
        return query
        
    def get_all(self):
        return self.db.view('_all_docs')
        
    def get_all_posts(self):
        return self.db.view('tulipblog/all')