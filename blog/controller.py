from db.database import CouchDBAdapter
from datetime import datetime


class BaseController(object):
    def __init__(self, **kwargs):
        self.db = CouchDBAdapter('tulipblog', 'http://xXxXxXxXxXx:xXxXxXxXxXx@localhost:5984/')


class HomeController(BaseController):
    def __init__(self, post_source='post', comment_source='comment', 
                 **kwargs):
        super(HomeController, self).__init__(**kwargs)
        self.blog_source = post_source
        self.comment_source = comment_source

    def store_query(self, query):
        query['datetime'] = datetime.now()
        return query

    def get_all(self):
        return self.db.view('_all_docs')

    def get_all_posts(self):
        return self.db.view(self.blog_source, 'all')

    def new_post(self, data):
        assert 'title' in data
        assert 'date' in data
        assert 'body' in data
