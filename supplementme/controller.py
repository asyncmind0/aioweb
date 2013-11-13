from controller import Controller


class NutrientsController(Controller):

    def __getitem__(self, name, default=None):
        pass

    def __setitem__(self, name, value):
        pass

    def keys(self):
        n = yield from self.db.view('nutrient', 'keys', group=True)
        if n and hasattr(n, 'rows'):
            return [d['key'] for d in n.rows]
        return []


class FoodController(Controller):
    pass