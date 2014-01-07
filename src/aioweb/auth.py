import asyncio
from aioweb.controller import Controller
import http.cookies
from uuid import uuid4
from aioweb.db.model import Model
from aioweb.session import Session


class User(Model):
    required_fields = ['username', 'password']
    views = {
        'by_username': {
            'map': """
                function(doc) {
                    if(doc.doc_type == 'User' && doc.username) {
                        emit(doc.username, doc);
                    }
                }
            """,
            'reduce': """
                function(keys, values){
                    return true;
                }
            """
        },
    }


class AuthController(Controller):
    @asyncio.coroutine
    def login(self, username, password):
        user = yield from User.view('by_username', self.db, key=username)
        user = user.first()
        return Session.start_session(user)


def authenticated(method):
    def _check_auth(self, request_args=None, **kwargs):
        sessionid = self.cookies.get('sessionid')
        userid = self.cookies.get('userid')
        if sessionid and userid:
            session = Session.get_session(userid.value, sessionid.value)
            assert session is not None, \
                UnAuthenticated("No session found please reauthenticate")
            self.session = session
        else:
            raise UnAuthenticated()
        yield from method(self, request_args=request_args, **kwargs)
    return _check_auth


class UnAuthenticated(Exception):
    def __init__(self, *args, msg='Unauthenticated request', **kwargs):
        super(UnAuthenticated, self).__init__(msg, *args, **kwargs)