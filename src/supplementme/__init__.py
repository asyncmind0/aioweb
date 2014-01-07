from os.path import join, dirname
from aioweb.static_handler import StaticFileHandler
from aioweb.router import Router
from .handler import (
    HomeHandler, FoodHandler, MealHandler, AuthHandler, NutrientHandler)


def get_routes():
    return Router("/", (
        ("/$", HomeHandler),
        ("/(supplementme)/(.*).js", StaticFileHandler, dict(
            staticroot=join(dirname(__file__), 'js'),
            baseurl="/supplementme/")),
        ("/(supplementme)/(.*).html", StaticFileHandler, dict(
            staticroot=join(dirname(__file__), 'html'),
            baseurl="/supplementme/")),
        ("/(supplementme)/(.*).css", StaticFileHandler, dict(
            staticroot=join(dirname(__file__), 'css'),
            baseurl="/supplementme/")),
        ("/auth/login$", AuthHandler),
        ("/meal/{0,1}(.*)$", MealHandler),
        ("/nutrients/{0,1}(.*)$", NutrientHandler),
        ("/food/{0,1}(.*)$", FoodHandler))
    )
