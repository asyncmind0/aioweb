from controller import Controller
from .model import Food, Nutrient


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
        assert hasattr(r, 'ok') and r.ok is True, "Failed to add food: %s" % str(r)


class ServingController(Controller):
    pass