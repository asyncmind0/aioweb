import re
import collections
from errors import ErrorHandlerMixin
import sys
import importlib
import imp


class Router(ErrorHandlerMixin):
    def __init__(self, basepath="/", handlers=None):
        super(Router, self).__init__()
        self.handlers = []
        if handlers:
            for handler in handlers:
                self.add_handler(*handler)

    def add_handler(self, url_regex, handlers, handler_args=None):
        if not handler_args:
            handler_args = {}
        self.handlers.append(
            [re.compile(url_regex), 
             handlers if isinstance(handlers, (collections.Iterable, Router))
             else [handlers], handler_args])

    def get_handler(self, url):
        for matcher, handler, handler_args in self.handlers:
            match = matcher.match(url)
            if match:
                if isinstance(handler, Router):
                    return handler.get_handler(url)
                return handler, match.groups(), handler_args
        return None, None, None

    def get_error_handler(self, url, exception):
        """Default router error handler"""
        return "TODO Error information"

    def reload_handlers(self, module_path=None):
        reload_modules = set()
        new_handlers = []
        reloaded_handlers = set()
        for t in self.handlers:
            matcher, handler_class_list, handler_args = t
            if isinstance(handler_class_list, Router):
                handler_class_list.reload_handlers(module_path)
            else:
                new_handler_class_list = []
                for handler_class in handler_class_list:
                    hmodule = handler_class.__module__
                    module = sys.modules[hmodule]
                    hmodule_path = module.__file__
                    if not module_path or (
                            module_path == hmodule_path 
                            and module_path not in reloaded_handlers):
                        print("Reloading:%s %s:%s" % (module_path, module, handler_class))
                        module = imp.reload(module)
                        reloaded_handlers.add(module_path)
                    new_handler_class_list.append(getattr(module, handler_class.__name__))
                t[1] = new_handler_class_list
            new_handlers.append(t)
        self.handlers = new_handlers
