import re
import collections

class Router(object):
    handlers = []

    def add_handler(self, url_regex, handlers):
        self.handlers.append(
            (re.compile(url_regex), 
             handlers if isinstance(handlers, collections.Iterable) 
             else [handlers]))

    def get_handler(self, url):
        for matcher, handler in self.handlers:
            match = matcher.match(url)
            if match:
                return handler, match.groups()
