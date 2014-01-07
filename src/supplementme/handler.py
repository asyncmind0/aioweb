import os
import logging
from aioweb.handler import Handler
from aioweb.renderers import HtmlRenderer, JsonRenderer
from .controller import (
    NutrientsController, MealController)
from .model import Nutrient
import asyncio
from aioweb.auth import AuthController, authenticated


class HomeHandler(Handler):
    renderer = HtmlRenderer([os.path.join(os.path.dirname(__file__), 'html')])

    def __call__(self, request_args=None, **kwargs):
        controller = NutrientsController()
        query = self.query
        keys = yield from controller.all()
        keys = [n for n in keys]
        logging.debug("number of nutrients: %s" % len(keys))
        scripts = []  # [{'src':'test.js'}]

        self.render('home', query=[{'key': key, 'value': value}
                                   for key, value in query.items()],
                    nutrients=keys, scripts=scripts)


class AuthHandler(Handler):
    renderer = JsonRenderer()

    @asyncio.coroutine
    def __call__(self, request_args=None, **kwargs):
        controller = AuthController()
        form = yield from self.get_form_data(True)
        session = yield from controller.login(
            form['username'].pop(), form['password'].pop())
        self.cookies = dict(userid=session.user._id, sessionid=session.id)
        self.render(**dict(ok=True))


class FoodHandler(Handler):
    renderer = JsonRenderer()

    @asyncio.coroutine
    def __call__(self, request_args=None, **kwargs):
        self.render(**dict(test='test'))


class MealHandler(Handler):
    renderer = JsonRenderer()

    @authenticated
    @asyncio.coroutine
    def __call__(self, request_args=None, **kwargs):
        self.controller = MealController(session=self.session)
        result = {}
        if 'add' in request_args:
            result = yield from self.add_meal()
        elif self.query.get('query'):
            result = yield from self.query_meals()
        self.render(**result)

    def add_meal(self):
        form = yield from self.get_form_data(True)
        form['user'] = self.session.user._id
        result = yield from self.controller.add_meal(form)
        return result.__dict__

    def query_meals(self):
        result = yield from self.controller.search_meals()
        return dict(data=[meal for meal in result])


class NutrientHandler(Handler):
    renderer = JsonRenderer()

    @asyncio.coroutine
    def __call__(self, request_args=None, **kwargs):
        self.controller = NutrientsController()
        result = yield from self.controller.all()
        self.render(result)
