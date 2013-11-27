import os
import logging
from handler import Handler
from renderers import HtmlRenderer, JsonRenderer
from .controller import NutrientsController
from .model import Nutrient
import tulip


class HomeHandler(Handler):
    renderer = HtmlRenderer([os.path.join(os.path.dirname(__file__), 'html')])

    def __call__(self, request_args=None, **kwargs):
        controller = NutrientsController(self.db)
        query = self.query
        keys = yield from Nutrient.all(self.db)
        keys = [n.data for n in keys.rows]
        logging.debug("number of nutrients: %s" % len(keys))
        scripts = [] #[{'src':'test.js'}]

        self.render('home', query=[{'key': key, 'value': value}
                                   for key, value in query.items()],
                    nutrients=keys, scripts=scripts)

class AddFoodHandler(Handler):
    renderer = JsonRenderer()
    @tulip.coroutine
    def __call__(self, request_args=None, **kwargs):
        self.render(**dict(test='test'))


class AddMealHandler(Handler):
    renderer = JsonRenderer()
    @tulip.coroutine
    def __call__(self, request_args=None, **kwargs):
        self.render(**dict(test='test'))