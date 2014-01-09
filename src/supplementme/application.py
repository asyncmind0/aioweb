from debug import pprint, pprintxml, shell, profile, debug as sj_debug, set_except_hook
import os
import imp
from aioweb.server import HttpServer
from aioweb.application import ProtocolFactory, main
from aioweb.router import Router
from aioweb.config import set_config
from aioweb.static_handler import StaticFileHandler
from os.path import join, dirname


def get_static_routes(router=None):
    from aioweb.config import config
    if not router:
        router = Router()
    router.add_handler(
        '/static/favicon.ico', StaticFileHandler,
        dict(staticroot=config['default']['staticroot']))
    router.add_handler(
        '/dojo/', StaticFileHandler, 
        dict(staticroot=join(dirname(__file__), 'static', 'dojo')))
    router.add_handler(
        '/dijit/', StaticFileHandler, 
        dict(staticroot=join(dirname(__file__), 'static', 'dojo')))
    router.add_handler(
        '/jasmine/', StaticFileHandler,
        dict(staticroot=join(dirname(__file__), 'static',
                             config['default']['jasmine']),
             baseurl='/jasmine/'))
    return router


class SupplementMeProtocolFactory(ProtocolFactory):

    def __call__(self):
        import supplementme
        imp.reload(supplementme)
        router = get_static_routes()
        router.add_handler('/', supplementme.get_routes())
        self.router = router
        return HttpServer(self.router, debug=True, keep_alive=75)


if __name__ == '__main__':
    base_path = os.path.dirname(__file__)
    set_config(base_path, 'development')
    set_except_hook()
    main(SupplementMeProtocolFactory)
