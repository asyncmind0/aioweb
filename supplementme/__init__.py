from os.path import join, dirname
from static_handler import StaticFileHandler
from .handler import HomeHandler, AddFoodHandler
from router import Router

def get_routes(db):
    return Router("/", (
        ("/$", HomeHandler(db)),
        ("/(supplementme)/(.*).js", StaticFileHandler(
            join(dirname(__file__), 'js'), baseurl="/supplementme/")),
        ("/(supplementme)/(.*).html", StaticFileHandler(
            join(dirname(__file__), 'html'), baseurl="/supplementme/")),
        ("/(supplementme)/(.*).css", StaticFileHandler(
            join(dirname(__file__), 'css'), baseurl="/supplementme/")),
        ("/add_food", AddFoodHandler(db)))
    )