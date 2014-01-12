from aioweb.db import get_db


class Controller():
    def __init__(self, db=None, session=None, **kwargs):
        self.session = session
        self._db = db

    @property
    def db(self):
        return self._db or get_db()
