import os
from aioweb.test import TestCase as BaseTestCase
from aioweb.db.couchdb_test import CouchDBTestCase


class TestCase(CouchDBTestCase):
    config_name="testing"
    base_path = os.path.dirname(__file__)