from uuid import uuid4


class Session:
    ACTIVE_SESSIONS = {}

    def __init__(self, user):
        self.user = user
        self.id = str(uuid4())

    @classmethod
    def get_session(cls, userid, sessionid):
        session = cls.ACTIVE_SESSIONS.get((userid, sessionid))
        return session

    @classmethod
    def start_session(cls, user):
        session = Session(user)
        return Session.ACTIVE_SESSIONS.setdefault(
            (user._id, session.id), session)
