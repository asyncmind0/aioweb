from aioweb.test import run_briefly
from .controller import Controller
from aioweb.db.model import Model
from aioweb.auth import User, AuthController
from aioweb.session import Session
from aioweb.db.couchdb_test import CouchDBTestCase


class ControllerTest (CouchDBTestCase):
    def setUp(self):
        super(ControllerTest, self).setUp()

