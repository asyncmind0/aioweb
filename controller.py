class Controller():
    def __init__(self, db, session=None,**kwargs):
        self.db = db
        self.session = session
