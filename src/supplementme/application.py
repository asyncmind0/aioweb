import os
import imp
from aioweb.server import HttpServer
from aioweb.application import ProtocolFactory, startapp
from aioweb.router import Router
from aioweb.config import set_config
from aioweb.static_handler import StaticFileHandler
from os.path import join, dirname
from supplementme.importer import import_sr25_nutr_def
from .model import (Meal, Food, Nutrient)
from aioweb.auth import User
import logging


def get_static_routes(router=None):
    from aioweb.config import config
    if not router:
        router = Router()
    router.add_handler('/favicon.ico', StaticFileHandler,
                       dict(staticroot=config['default']['staticroot']))
    router.add_handler('/dojo/', StaticFileHandler,
                       dict(staticroot=config['default']['dojo'],
                            baseurl="/dojo/"))
    router.add_handler('/jasmine/', StaticFileHandler,
                       dict(staticroot=config['default']['jasmine'],
                            baseurl='/jasmine/'))
    return router


class SupplementMeProtocolFactory(ProtocolFactory):

    def __call__(self):
        try:
            import supplementme
            imp.reload(supplementme)
            router = get_static_routes()
            router.add_handler('/', supplementme.get_routes())
            self.router = router
            return HttpServer(self.router, debug=True, keep_alive=75)
        except Exception as e:
            logging.exception("Failed to create HttpServer")


def init_database():
    """Initialize database push all design documents
    """
    import asyncio
    loop = asyncio.get_event_loop()
    from aioweb.db import get_db
    db = get_db()
    # need to import model to get them registered in the metaclass registry
    loop.run_until_complete(db.sync_designs(db))
    loop.run_until_complete(import_sr25_nutr_def(db))


def main():
    base_path = os.path.dirname(__file__)
    set_config(base_path, 'development')
    logging.getLogger('static_paths').setLevel(logging.INFO)
    init_database()
    startapp(SupplementMeProtocolFactory)

if __name__ == '__main__':
    main()
