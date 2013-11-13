import os
import logging
from handler import Handler
from renderers import HtmlRenderer
from .controller import NutrientsController
from .model import Nutrient


class HomeHandler(Handler):
    renderer = HtmlRenderer([os.path.dirname(__file__)])

    def __call__(self, request_args=None, **kwargs):
        controller = NutrientsController(self.db)
        query = self.query
        keys = yield from Nutrient.all(self.db)
        keys = [n.data for n in keys.rows]
        logging.debug("number of nutrients: %s" % len(keys))

        self.render('home', query=[{'key': key, 'value': value}
                                   for key, value in query.items()],
                    nutrients=keys)
