import os
import logging
from aioweb.handler import Handler
from aioweb.renderers import HtmlRenderer, JsonRenderer
from .controller import (
    NutrientsController, MealController, FoodController)
from .model import Nutrient, Food, Meal
import asyncio
from aioweb.auth import AuthController, authenticated
import json
from .forms import AuthForm


class HomeHandler(Handler):
    renderer = HtmlRenderer([os.path.join(os.path.dirname(__file__), 'html')])

    def __call__(self, request_args=None, **kwargs):
        controller = NutrientsController()
        query = self.query
        keys = yield from controller.all()
        logging.debug("number of nutrients: %s" % len(keys))
        scripts = [{'src': '/supplementme/main_test.js'},
                   {'src': '/supplementme/main.js'}]

        body = self.renderer.render(
            "home", query=[
                {'key': key, 'value': value}
                for key, value in query.items()],
            nutrients=keys)
        self.render('base', body=body, scripts=scripts)


class AuthHandler(Handler):
    renderer = JsonRenderer()

    @asyncio.coroutine
    def __call__(self, request_args=None, **kwargs):
        controller = AuthController()
        form = yield from self.get_form_data(True)
        session = yield from controller.login(
            form['username'].pop(), form['password'].pop())
        self.cookies = dict(userid=session.user._id, sessionid=session.id)
        form = AuthForm()
        self.render(**dict(ok=True))


class FoodHandler(Handler):
    renderer = JsonRenderer()

    @asyncio.coroutine
    def __call__(self, request_args=None, **kwargs):
        controller = FoodController()
        if request_args and 'add' in request_args:
            form = yield from self.get_form_data(True)
            food = dict(
                name=form['name'][0],
                serving_size=form['serving_size'][0],
                unit=form['unit'][0],
                nutrients=json.loads(form['nutrients'][0]))
            print(food)
            food = yield from controller.add_update_food(food)
            assert hasattr(food, '_id'), str(food)
            self.render(**dict(food=food.data))
        else:
            foods = yield from Food.all(controller.db)

            self.render([food for food in foods])


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


class WidgetTestHandler(Handler):
    renderer = HtmlRenderer([os.path.join(os.path.dirname(__file__), 'html')])

    def __call__(self, request_args=None, **kwargs):
        controller = NutrientsController()
        query = self.query
        keys = yield from controller.all()
        logging.debug("number of nutrients: %s" % len(keys))
        #scripts = [{'src': '/supplementme/NutrientWidget_test.js'},
        #           {'src': '/supplementme/NutrientWidget.js'}]
        scripts = []

        body = self.renderer.render(
            "%s_test" % request_args[0], query=[
                {'key': key, 'value': value}
                for key, value in query.items()],
            nutrients=keys)
        self.render('base', body=body, scripts=scripts)