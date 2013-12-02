import os
import logging
from handler import Handler
from renderers import HtmlRenderer, JsonRenderer
from .controller import (
    NutrientsController, MealController)
from .model import Nutrient
import tulip
from tulip.http.protocol import http_payload_parser
from auth import AuthController, authenticated


class HomeHandler(Handler):
    renderer = HtmlRenderer([os.path.join(os.path.dirname(__file__), 'html')])

    def __call__(self, request_args=None, **kwargs):
        controller = NutrientsController(self.db)
        query = self.query
        keys = yield from Nutrient.all(self.db)
        keys = [n.data for n in keys.rows]
        logging.debug("number of nutrients: %s" % len(keys))
        scripts = []  # [{'src':'test.js'}]

        self.render('home', query=[{'key': key, 'value': value}
                                   for key, value in query.items()],
                    nutrients=keys, scripts=scripts)


class AuthHandler(Handler):
    renderer = JsonRenderer()

    @tulip.coroutine
    def __call__(self, request_args=None, **kwargs):
        controller = AuthController(self.db)
        form = self.get_form_data(True)
        session = yield from controller.login(form['username'].pop(), form['password'].pop())
        self.cookies = dict(userid=session.user._id, sessionid=session.id)
        self.render(**dict(ok=True))


class AddFoodHandler(Handler):
    renderer = JsonRenderer()

    @tulip.coroutine
    def __call__(self, request_args=None, **kwargs):
        self.render(**dict(test='test'))


class MealHandler(Handler):
    renderer = JsonRenderer()

    @authenticated
    @tulip.coroutine
    def __call__(self, request_args=None, **kwargs):
        controller = MealController(self.db, session=self.session)
        result = {}
        if 'add' in request_args:
            form = self.get_form_data(True)
            form['user'] = self.session.user._id
            result = yield from controller.add_meal(form)
            result = result.__dict__
        elif self.query.get('query'):
            result = yield from controller.search_meals()
            result = dict(data=[meal for meal in result])
        self.render(**result)
