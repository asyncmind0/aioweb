from aioweb.db import get_db


class Controller():
    def __init__(self, db=None, session=None,**kwargs):
        self.session = session

    @property
    def db(self):
        return get_db()
