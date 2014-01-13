import sys
import asyncio
import inspect
import logging


def catch_db_exception(func):
    """Decorator to catch exceptions

    """
    def catch_exception(*args, **kwargs):
        try:
            if inspect.isgeneratorfunction(func):
                coro = func(*args, **kwargs)
                exc = coro.exception()
                if exc:
                    raise exc
            else:
                return func(*args, **kwargs)
        except asyncio.ConnectionRefusedError as e:
            logging.error('Could not connect to couchdb')
            import os
            import signal
            os.kill(os.getpid(), signal.SIGTERM)
            sys.exit(1)
    return catch_exception


class Bunch():
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        return str(self.__dict__)


class ResultList(Bunch):
    def __len__(self):
        if 'total_rows' in self.__dict__:
            return self.total_rows
        else:
            return 0

    def __iter__(self):
        for row in self.__dict__['rows']:
            yield row['value']

    def first(self):
        if 'total_rows' in self.__dict__ and \
           self.__dict__['total_rows'] > 0:
            return self.__dict__['rows'][0]['value']
        return None

    def last(self):
        if 'total_rows' in self.__dict__ and \
           self.__dict__['total_rows'] > 0:
            return self.__dict__['rows'][-1]['value']
        return None


class DatabaseAdapter:
    pass


