from os.path import join, dirname
from static_handler import StaticFileHandler
from .handler import (
    HomeHandler, FoodHandler, MealHandler, AuthHandler, NutrientHandler)
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
        ("/auth/login$", AuthHandler(db)),
        ("/meal/{0,1}(.*)$", MealHandler(db)),
        ("/nutrients/{0,1}(.*)$", NutrientHandler(db)),
        ("/food/{0,1}(.*)$", FoodHandler(db)))
    )
