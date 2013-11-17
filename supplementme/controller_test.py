from test import CouchDBTestCase
from .controller import NutrientsController, FoodController
from .model import Nutrient, Food


class ControllerTest (CouchDBTestCase):
    def setUp(self):
        super(ControllerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.controller = NutrientsController(self.db)
        self.test_nutrients = [
            Nutrient(number=10, name='vitamin c', tag='vitc', decimal_places=3, unit='mg'),
            Nutrient(number=10, name='vitamin d', tag='vitd', decimal_places=3, unit='mg')
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


class FoodControllerTest (CouchDBTestCase):
    def setUp(self):
        super(FoodControllerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.loop.run_until_complete(Food.sync_design(self.db))
        self.controller = FoodController(self.db)

    def tearDown(self):
        super(FoodControllerTest, self).tearDown()

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
        r = self.loop.run_until_complete(Food.get(r.id,self.db))
        assert r.name == 'somefood'
        assert hasattr(r, 'serving_size') and r.serving_size == 300, str(r)

    def test_all(self):
        self.test_add_food()
        r = self.loop.run_until_complete(Food.all(self.db))
        assert hasattr(r, 'rows') and len(r.rows) > 0, str(r)

    def test_nutrient_totals(self):
        pass
