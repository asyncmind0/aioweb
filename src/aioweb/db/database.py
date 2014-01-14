import sys
import asyncio
import inspect
import logging


class Bunch():
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    def __str__(self):
        return str(self.__dict__)


class DatabaseAdapter:
    pass
