import tulip
from controller import Controller
from .model import Food, Nutrient, Meal
from auth import User
import http.cookies
from uuid import uuid4
from session import Session


class NutrientsController(Controller):

    def __getitem__(self, name, default=None):
        pass

    def __setitem__(self, name, value):
        assert isinstance(value, Nutrient)
        pass

    def keys(self):
        n = yield from self.db.view('nutrient', 'keys', group=True)
        if n and hasattr(n, 'rows'):
            return [d['key'] for d in n.rows]
        return []


class FoodController(Controller):
    def get_foods(self, name):
        r = yield from Food.all(self.db)
        assert hasattr(r, 'rows') and len(r.rows) > 0, str(r)
        return r.rows

    def add_update_food(self, name, value):
        assert isinstance(value, Food), "Invalid value"
        old_food = None
        if '_id' in food and food._id:
            old_food = yield from Food.get(_id)
        else:
            old_food = yield from Food.view('by_name', self.db)
            old_food = old_food[0]
        if old_food:
            old_food.update(food)
            food = old_food

        r = yield from food.save(self.db)
        assert hasattr(
            r, 'ok') and r.ok is True, "Failed to add food: %s" % str(r)


class MealController(Controller):
    @tulip.coroutine
    def all_meals(self):
        meals = yield from Meal.all(self.db)
        return meals

    @tulip.coroutine
    def add_meal(self, meal):
        meal = Meal(**meal)
        save = yield from meal.save(self.db)
        return save

    @tulip.coroutine
    def search_meals(self):
        meals = yield from Meal.view('by_user', self.db, key=self.session.user._id)
        return meals


class UserController(Controller):
    @tulip.coroutine
    def add_user(self, user):
        user = User(**user)
        save = yield from user.save(self.db)
        return save
