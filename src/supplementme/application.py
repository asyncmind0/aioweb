import os
import imp
import aioweb
import supplementme
from aioweb.server import HttpServer
from aioweb.application import ProtocolFactory, startapp
from aioweb.router import Router
from aioweb.config import set_config, configure_logging
from aioweb.static_handler import StaticFileHandler
from os.path import join, dirname
from supplementme.importer import import_sr25_nutr_def
from supplementme.model import (Meal, Food, Nutrient)
from supplementme.routes import get_routes
from aioweb.auth import User
import logging


class SupplementMeProtocolFactory(ProtocolFactory):

    def __call__(self):
        try:
            import supplementme
            imp.reload(supplementme)
            router = get_routes()
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
    configure_logging(base_path)
    init_database()
    startapp(SupplementMeProtocolFactory)

if __name__ == '__main__':
    main()
