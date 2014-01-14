from aioweb.test import run_briefly
from .controller import (
    NutrientsController, FoodController, MealController,
    UserController)
from .model import Nutrient, Food, Meal
from aioweb.auth import User, AuthController
from aioweb.session import Session
from aioweb.db.couchdb_test import CouchDBTestCase
from aioweb.controller_test import ControllerTest as BaseControllerTest
from .importer import import_sr25_nutr_def
from nose.tools import nottest


class ControllerTest (BaseControllerTest):
    def setUp(self):
        super(ControllerTest, self).setUp()
        self.loop.run_until_complete(import_sr25_nutr_def(self.db))
        self.test_food = dict(name="somefood",
                              nutrients={'ALC': dict(quantity=10),
                                         'ASH': dict(quantity=20),
                                         'CAFFN': dict(quantity=10),
                                         'BETN': dict(quantity=20)},
                              serving_size=300,
                              unit='mg')


class AuthControllerTest (ControllerTest):
    def setUp(self):
        super(AuthControllerTest, self).setUp()
        self.loop.run_until_complete(self.db.sync_designs())
        self.user_controller = UserController(self.db)
        self.auth_controller = AuthController(self.db)
        self.test_user = 'testuser'
        r = self.loop.run_until_complete(
            self.user_controller.add_user(
                dict(username='testuser', password='testpass')))
        assert hasattr(r, 'ok') and r.ok is True, str(r)
        self.userid = r.id
        self.test_pass = 'password'

    def test_login(self):
        r = self.loop.run_until_complete(
            self.auth_controller.login(self.test_user, self.test_pass))
        assert isinstance(r, Session), r
        assert isinstance(r.user, User), r.user
        assert isinstance(r.id, str)
        self.session = r


class FoodControllerTest (AuthControllerTest):
    def setUp(self):
        super(FoodControllerTest, self).setUp()
        self.test_login()
        self.controller = FoodController(self.db, session=self.session)
        self.loop.run_until_complete(import_sr25_nutr_def(self.db))

    def test_add_food(self):
        food = self.loop.run_until_complete(
            self.controller.add_update_food(self.test_food))
        assert hasattr(food, '_id') and food.name == "somefood", str(food)

    def test_update_food(self):
        food = self.loop.run_until_complete(
            self.controller.add_update_food(self.test_food))
        assert hasattr(food, '_id') and food.name == "somefood", str(food)
        assert hasattr(food, 'serving_size') and food.serving_size == 300, str(food)

    def test_all(self):
        self.test_add_food()
        r = self.loop.run_until_complete(Food.all(self.db))
        assert hasattr(r, 'rows') and len(r.rows) > 0, str(r)

    def test_nutrient_totals(self):
        pass


class MealControllerTest (AuthControllerTest):
    def setUp(self):
        super(MealControllerTest, self).setUp()
        self.loop.run_until_complete(import_sr25_nutr_def(self.db))
        self.test_login()
        self.controller = MealController(session=self.session)
        self.food_controller = FoodController(session=self.session)

    def test_add_meal(self):
        food = self.loop.run_until_complete(
            self.food_controller.add_update_food(self.test_food))
        assert hasattr(food, '_id') and food.name == "somefood", str(food)
        meal = dict(foods=[food._id], quantity='200g', user=self.userid)
        r = self.loop.run_until_complete(self.controller.add_meal(meal))
        assert hasattr(r, 'ok') and r.ok is True, str(r)

    def test_search_meal(self):
        self.test_add_meal()
        r = self.loop.run_until_complete(
            self.controller.search_meals())
        assert hasattr(r, 'total_rows') and r.total_rows > 0, str(r)


class NutrientControllerTest (AuthControllerTest):
    def setUp(self):
        super(NutrientControllerTest, self).setUp()
        self.controller = NutrientsController(self.db)
        self.test_login()
        self.test_nutrients = [
            Nutrient(number=10, name='vitamin c', tag='vitc',
                     decimal_places=3, unit='mg'),
            Nutrient(number=10, name='vitamin d', tag='vitd',
                     decimal_places=3, unit='mg')
        ]

    def test_list_nutrients(self):
        r = self.loop.run_until_complete(
            self.controller.all())
        assert len(r) > 0, r

    def test_new(self):
        for nut in self.test_nutrients:
            r = self.loop.run_until_complete(nut.save(self.db))
            assert hasattr(r, 'ok') and r.ok is True, str(r)

    def test_all(self):
        self.test_new()
        r = self.loop.run_until_complete(Nutrient.all(self.db))
        assert len(r.rows) > 0, str(r)

    @nottest
    def test_keys(self):
        self.test_new()
        r = self.loop.run_until_complete(self.controller.keys())
        assert len(r) > 0, str(r)
        test_names = [n.tag for n in self.test_nutrients]
        self.assertListEqual(sorted(r), sorted(test_names)), str(r)