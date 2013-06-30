from database import get_db
from datetime import datetime


class BaseController(object):
    def __init__(self, *args, **kwargs):
        self.db = get_db()


class HomeController(BaseController):
    def __init__(self, *args, **kwargs):
        super(HomeController, self).__init__(*args, **kwargs)

    def store_query(self, query):
        query['datetime'] = datetime.now()
        return query
        
    def get_all(self):
        return self.db.all('id')
        
    def get_all_posts(self):
        return self.db.view('blog/all')
