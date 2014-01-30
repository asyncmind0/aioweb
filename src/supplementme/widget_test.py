from debug import pprint, pprintxml, shell, profile, debug as sj_debug
import os
import sys
import json

import asyncio
from asyncio import streams
from asyncio import protocols

from subprocess import Popen, PIPE
from .test import TestCase
from aioweb.test import run_test_server
from aioweb.db.couchdb_test import CouchDBTestCase
from .routes import get_routes
from .model import Nutrient, Meal
from aioweb.auth import User
from .importer import import_sr25_nutr_def
from nose.tools import nottest as broken

from .functional_tests import FunctionalTest


class NutientTest(FunctionalTest):
    def test_load(self):
        self._test_page("/test/nutrientwidget", pause=True)