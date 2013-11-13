from test import CouchDBTestCase
from .controller import NutrientsController, FoodController
from .model import Nutrient, Food


class ControllerTest (CouchDBTestCase):
    def setUp(self):
        super(ControllerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.controller = NutrientsController(self.db)

    def tearDown(self):
        super(ControllerTest, self).tearDown()

    def test_new(self, name='vitamin_c'):
        post = Nutrient(quantity=10, name=name)
        r = self.loop.run_until_complete(post.save(self.db))
        assert hasattr(r, 'ok') and r.ok is True, str(r)

    def test_all(self):
        self.test_new()
        r = self.loop.run_until_complete(Nutrient.all(self.db))
        assert len(r.rows) > 0, str(r)

    def test_keys(self):
        test_names = ['vitamin_d', 'vitamin_c']
        self.test_new(test_names[0])
        self.test_new(test_names[0])
        self.test_new(test_names[0])
        self.test_new()
        self.test_new()
        r = self.loop.run_until_complete(self.controller.keys())
        assert len(r) > 0, str(r)
        self.assertListEqual(sorted(r), sorted(test_names)), str(r)


class FoodControllerTest (CouchDBTestCase):
    def setUp(self):
        super(FoodControllerTest, self).setUp()
        self.loop.run_until_complete(Nutrient.sync_design(self.db))
        self.controller = FoodController(self.db)

    def tearDown(self):
        super(FoodControllerTest, self).tearDown()

    def test_new(self):
        food = Food(name="somefood",
                    nutrients=[['vitamin_c', 10], ['vitamin_d', 20]],
                    quantity=200)
        r = self.loop.run_until_complete(food.save(self.db))
        assert hasattr(r, 'ok') and r.ok is True, str(r)

    def test_all(self):
        self.test_new()
        r = self.loop.run_until_complete(Food.all(self.db))
        assert len(r.rows) > 0, str(r)

    def test_nutrient_totals(self):
        pass
