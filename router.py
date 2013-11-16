import re
import collections
from errors import ErrorHandlerMixin


class Router(ErrorHandlerMixin):
    def __init__(self, basepath="/", handlers=None):
        super(Router, self).__init__()
        self.handlers = []
        if handlers:
            for handler in handlers:
                self.add_handler(*handler)

    def add_handler(self, url_regex, handlers):
        self.handlers.append(
            (re.compile(url_regex), 
             handlers if isinstance(handlers, (collections.Iterable, Router))
             else [handlers]))

    def get_handler(self, url):
        for matcher, handler in self.handlers:
            match = matcher.match(url)
            if match:
                if isinstance(handler, Router):
                    return handler.get_handler(url)
                return handler, match.groups()
        return None, None

    def get_error_handler(self, url, exception):
        """Default router error handler"""
        return "TODO Error information"
