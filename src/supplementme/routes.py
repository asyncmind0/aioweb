from os.path import join, dirname
from aioweb.static_handler import StaticFileHandler
from aioweb.router import Router
from .handler import (
    HomeHandler, FoodHandler, MealHandler, AuthHandler, NutrientHandler, 
    WidgetTestHandler)


def get_routes(router=None):
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

    app_routes = Router("/", (
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
        ("/food/{0,1}(.*)$", FoodHandler),
        ("/test/{0,1}(.*)$", WidgetTestHandler))
    )
    router.add_handler('/', app_routes)
    return router