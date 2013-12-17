from db import get_db


class Controller():
    def __init__(self, db=None, session=None,**kwargs):
        self.db = db or get_db()
        self.session = session
