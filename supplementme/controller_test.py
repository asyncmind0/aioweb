from test import CouchDBTestCase
from .controller import (
    NutrientsController, FoodController, MealController,
    UserController)
from .model import Nutrient, Food, Meal
from auth import User, AuthController
from session import Session


class ControllerTest (CouchDBTestCase):
    def setUp(self):
        super(ControllerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.controller = NutrientsController(self.db)
        self.test_nutrients = [
            Nutrient(number=10, name='vitamin c', tag='vitc',
                     decimal_places=3, unit='mg'),
            Nutrient(number=10, name='vitamin d', tag='vitd',
                     decimal_places=3, unit='mg')
        ]

    def tearDown(self):
        super(ControllerTest, self).tearDown()

    def test_new(self):
        for nut in self.test_nutrients:
            r = self.loop.run_until_complete(nut.save(self.db))
            assert hasattr(r, 'ok') and r.ok is True, str(r)

    def test_all(self):
        self.test_new()
        r = self.loop.run_until_complete(Nutrient.all(self.db))
        assert len(r.rows) > 0, str(r)

    def test_keys(self):
        self.test_new()
        r = self.loop.run_until_complete(self.controller.keys())
        assert len(r) > 0, str(r)
        test_names = [n.name for n in self.test_nutrients]
        self.assertListEqual(sorted(r), sorted(test_names)), str(r)

class AuthControllerTest (CouchDBTestCase):
    def setUp(self):
        super(AuthControllerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.loop.run_until_complete(Food.sync_design(self.db))
        self.loop.run_until_complete(Meal.sync_design(self.db))
        self.loop.run_until_complete(User.sync_design(self.db))
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


class FoodControllerTest (AuthController):
    def setUp(self):
        super(FoodControllerTest, self).setUp()
        self.controller = FoodController(self.db)
        self.test_login()

    def test_add_food(self):
        food = Food(name="somefood",
                    nutrients=[['vitamin_c', 10], ['vitamin_d', 20]],
                    serving_size=200,
                    unit='mg')
        r = self.loop.run_until_complete(food.save(self.db))
        assert hasattr(r, 'ok') and r.ok is True, str(r)

    def test_update_food(self):
        food = Food(name="somefood",
                    nutrients=[['vitamin_c', 10], ['vitamin_d', 20]],
                    serving_size=300,
                    unit='mg')
        r = self.loop.run_until_complete(food.save(self.db))
        assert hasattr(r, 'ok') and r.ok is True, str(r)
        r = self.loop.run_until_complete(Food.get(r.id, self.db))
        assert r.name == 'somefood'
        assert hasattr(r, 'serving_size') and r.serving_size == 300, str(r)

    def test_all(self):
        self.test_add_food()
        r = self.loop.run_until_complete(Food.all(self.db))
        assert hasattr(r, 'rows') and len(r.rows) > 0, str(r)

    def test_nutrient_totals(self):
        pass


class MealControllerTest (AuthController):
    def setUp(self):
        super(MealControllerTest, self).setUp()
        self.test_login()


    def test_add_meal(self):
        food = Food(name="somefood",
                    nutrients=[['vitamin_c', 10], ['vitamin_d', 20]],
                    serving_size=300,
                    unit='mg')
        r = self.loop.run_until_complete(food.save(self.db))
        assert hasattr(r, 'ok') and r.ok is True, str(r)
        meal = dict(foods=[food._id], quantity='200g', user=self.userid)
        r = self.loop.run_until_complete(self.controller.add_meal(meal))
        assert hasattr(r, 'ok') and r.ok is True, str(r)

    def test_search_meal(self):
        self.test_add_meal()
        r = self.loop.run_until_complete(
            self.controller.search_meals())
        assert hasattr(r, 'total_rows') and r.total_rows > 0, str(r)


