import tulip
import tulip.http
from base_handler import BaseHandler
from renderers import HtmlRenderer
from controller import HomeController

class HomeHandler(BaseHandler):
    renderer = HtmlRenderer()
    def __call__(self, request_args=None):
        controller = HomeController()
        query = controller.store_query(self.query)
        posts = controller.get_all_posts()
        self.render('home', query=[{'key': key, 'value': value} 
                                   for key, value in query.items()])
