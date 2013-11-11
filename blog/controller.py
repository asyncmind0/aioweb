from db.database import CouchDBAdapter
from datetime import datetime


class BaseController(object):
    def __init__(self, **kwargs):
        pass


class HomeController(BaseController):
    def __init__(self, db, post_source='post', comment_source='comment', 
                 **kwargs):
        super(HomeController, self).__init__(**kwargs)
        self.db = db
        self.blog_source = post_source
        self.comment_source = comment_source

    def store_query(self, query):
        query['datetime'] = datetime.now()
        return query

    def get_all_posts(self):
        posts = yield from self.db.view(self.blog_source, 'all')
        return posts

    def new_post(self, model):
        assert 'title' in model.data
        assert 'date' in model.data
        assert 'body' in model.data
        r = yield from self.db.put(model.data)
        return r.ok == True
