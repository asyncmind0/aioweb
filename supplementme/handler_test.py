from debug import pprint, pprintxml, shell, profile, debug as sj_debug
import unittest
import unittest.mock
from test import CouchDBTestCase
from test import TestCase, run_test_server
from .handler import (HomeHandler, FoodHandler, MealHandler, AuthHandler,
                      NutrientHandler)
from .controller import UserController
from .model import Nutrient, Food, Meal
from auth import User
from . import get_routes
import tulip
from tulip.http import client
import json
from .importer import import_sr25_nutr_def


class HomeHandlerTest(CouchDBTestCase):
    def setUp(self):
        super(HomeHandlerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.handler = HomeHandler(self.db)
        self.transport = unittest.mock.Mock()
        self.handler.response = self.transport

    def tearDown(self):
        super(HomeHandlerTest, self).tearDown()

    def test_home(self):
        r = self.loop.run_until_complete(self.handler())
        assert self.transport.write.called is True, "write Not called"
        assert len(self.transport.write.call_args[0][0]) > 0


class AuthHandlerTest(CouchDBTestCase):
    def setUp(self):
        super(AuthHandlerTest, self).setUp()
        self.loop.run_until_complete(User.sync_design(self.db))
        self.auth_handler = AuthHandler(self.db)
        transport = unittest.mock.Mock()
        self.auth_handler.response = transport
        self.test_user = 'testuser'
        # probably shoudl replace this with actual signup...
        self.user_controller = UserController(self.db)
        r = self.loop.run_until_complete(
            self.user_controller.add_user(
                dict(username='testuser', password='testpass')))
        assert hasattr(r, 'ok') and r.ok is True, str(r)
        self.userid = r.id
        self.test_pass = 'password'
        self.cookies = None

    def test_login(self):
        with run_test_server(self.loop, router=get_routes(self.db)) as httpd:
            url = httpd.url('auth', 'login')
            data = dict(username=self.test_user, password=self.test_pass)
            meth = 'post'
            r = self.loop.run_until_complete(
                client.request(meth, url, data=data))
            content1 = self.loop.run_until_complete(r.read())
            content = content1.decode()
            resp = json.loads(content)

            self.assertEqual(r.status, 200)
            assert 'ok' in resp
            assert r.cookies['userid'].value
            assert r.cookies['sessionid'].value
            self.cookies = r.cookies
            r.close()


class AddFoodHandlerTest(CouchDBTestCase):
    def setUp(self):
        super(AddFoodHandlerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.handler = AddFoodHandler()
        self.transport = unittest.mock.Mock()
        self.handler.response = self.transport

    def test_add_food(self):
        r = self.loop.run_until_complete(self.handler())
        assert self.transport.write.called is True, "write Not called"
        assert len(self.transport.write.call_args[0][0]) > 0


class MealHandlerTest(AuthHandlerTest):
    def setUp(self):
        super(MealHandlerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.loop.run_until_complete(Meal.sync_design(self.db))
        self.handler = AddFoodHandler()
        self.transport = unittest.mock.Mock()
        self.handler.response = self.transport

    def test_add_meal(self):
        self.test_login()
        with run_test_server(self.loop, router=get_routes(self.db)) as httpd:
            url = httpd.url('meal', 'add')
            meth = 'post'
            food = dict(name="somefood",
                        nutrients=[['vitamin_c', 10], ['vitamin_d', 20]],
                        serving_size=300,
                        unit='mg')
            meal = dict(foods=[food], quantity='200g')
            r = self.loop.run_until_complete(
                client.request(meth, url, data=meal, cookies=self.cookies))
            content1 = self.loop.run_until_complete(r.read())
            content = content1.decode()
            resp = json.loads(content)

            self.assertEqual(r.status, 200)
            assert 'ok' in resp, resp
            r.close()

    def test_search_meal(self):
        self.test_add_meal()
        with run_test_server(self.loop, router=get_routes(self.db)) as httpd:
            url = httpd.url('meal')
            params = (('query', 'name'),)
            meth = 'get'
            r = self.loop.run_until_complete(
                client.request(meth, url, params=params, cookies=self.cookies))
            content1 = self.loop.run_until_complete(r.read())
            content = content1.decode()
            resp = json.loads(content)

            self.assertEqual(r.status, 200)
            assert 'data' in resp, resp
            assert isinstance(resp['data'], list), resp['data']
            assert len(resp['data']) > 0, resp['data']
            for meal in resp['data']:
                assert 'foods' in meal, meal
            r.close()


class NutrientHandlerTest(AuthHandlerTest):
    def setUp(self):
        super(NutrientHandlerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.loop.run_until_complete(Meal.sync_design(self.db))
        self.handler = NutrientHandler()
        self.transport = unittest.mock.Mock()
        self.handler.response = self.transport
        import_sr25_nutr_def(self.db, self.loop)

    def test_list_nutrients(self):
        self.test_login()
        with run_test_server(self.loop, router=get_routes(self.db)) as httpd:
            url = httpd.url('nutrients')
            params = (('query', 'name'),)
            meth = 'get'
            r = self.loop.run_until_complete(
                client.request(meth, url, params=params, cookies=self.cookies))
            content1 = self.loop.run_until_complete(r.read())
            content = content1.decode()
            resp = json.loads(content)

            self.assertEqual(r.status, 200)
            assert isinstance(resp, list), resp
            assert len(resp) > 0, resp
            r.close()