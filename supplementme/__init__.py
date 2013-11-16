from os.path import join, dirname
from static_handler import StaticFileHandler
from .handler import HomeHandler
from router import Router

def get_routes(db):
    return Router("/", (("/$", HomeHandler(db)),
              ("/(.*).js", StaticFileHandler(join(dirname(__file__), 'js'))))
              ("/add_food", AddFoodHandler(db))
    )