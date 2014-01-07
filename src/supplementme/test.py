import os
from aioweb.test import TestCase as BaseTestCase

class TestCase(BaseTestCase):
    config_name="testing"
    base_path = os.path.dirname(__file__)