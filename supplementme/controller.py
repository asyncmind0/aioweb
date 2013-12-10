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
        return [d['key'] for d in n.rows]

    def validate_nutrients(self, nutrient_tags):
        validated = yield from Nutrient.view(
            'by_tag', self.db, keys=nutrient_tags)
        assert len(validated.rows) == len(nutrient_tags) \
            and set(nutrient_tags) == set([n['key'] for n in validated.rows]),\
            "Invalid Nutrients"


class FoodController(Controller):
    def get_foods(self, name):
        r = yield from Food.all(self.db)
        assert hasattr(r, 'rows') and len(r.rows) > 0, str(r)
        return r.rows

    def add_update_food(self, value):
        assert isinstance(value, dict), "Invalid value"
        name = value['name']
        food = Food(**value)
        nutrient_controller = NutrientsController(self.db)
        yield from nutrient_controller.validate_nutrients(
            [n['tag'] for n in food.nutrients])
        old_food = None
        if food._id:
            old_food = yield from Food.get(_id)
        else:
            old_food = yield from Food.view('by_name', self.db)
            old_food = old_food.first()
        if old_food:
            old_food.update(food)
            food = old_food

        r = yield from food.save(self.db)
        return r


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
