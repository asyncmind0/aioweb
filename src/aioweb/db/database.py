import sys
import json
import asyncio
import aiohttp
from urllib.parse import quote, urlencode
from urllib.request import urljoin
from uuid import uuid4
import inspect
import logging
import sys
from .model_codecs import json_dumps, json_loads


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
        except ConnectionRefusedError as e:
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


class CouchDBError(Exception):
    pass


class DatabaseAdapter:
    pass


class CouchDBAdapter(DatabaseAdapter):
    def __init__(self, url, dbname=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self._url = url
        self._dbname = dbname

    @property
    def _dburl(self):
        return urljoin(self._url, self._dbname + '/')

    def info(self, doc_id=None):
        url = self._dburl
        if doc_id:
            url = urljoin(url, doc_id)
        response = yield from aiohttp.request(
            'GET', url,
            headers={
                'Accept': 'application/json'
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    @asyncio.coroutine
    def create_db(self, dbname=None, **options):
        if not dbname:
            dbname = self._dbname
        response = yield from aiohttp.request(
            'PUT', urljoin(self._url, dbname),
            headers={
                'Accept': 'application/json'
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    def delete_db(self, dbname=None, **options):
        if not dbname:
            dbname = self._dbname
        response = yield from aiohttp.request(
            'DELETE', urljoin(self._url, dbname),
            headers={
                'Accept': 'application/json'
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    def put(self, document, doc_id=None, **options):
        if not isinstance(document, dict):
            document = document.__dict__
        document = {key: val for key, val in document.items(
        ) if not key.startswith('__')}
        if not doc_id:
            doc_id = document.get('_id', document.get('id'))
        if 'id' in document:
            del document['id']
        if '_id' in document:
            del document['_id']
        if '_rev' in document and not document['_rev']:
            del document['_rev']
        if not doc_id:
            doc_id = str(uuid4())
        posturl = urljoin(self._dburl, doc_id)
        response = yield from aiohttp.request(
            'POST', self._dburl, data=json_dumps(document),
            headers={
                'Accept': 'application/json',
                'content-type': 'application/json'
            })
        data = yield from response.read()
        data = json_loads(data)
        if 'ok' in data and data['ok'] is True:
            document['_id'] = data['id']
            document['_rev'] = data['rev']
        return Bunch(**data)

    def get(self, doc_id, **options):
        response = yield from aiohttp.request(
            'GET', urljoin(self._dburl, doc_id),
            headers={
                'Accept': 'application/json'
            })
        data = yield from response.read()
        return json_loads(data)

    def delete(self, doc_id, rev=None, **options):
        if rev == None:
            rev = yield from self.info(doc_id)
            rev = rev._rev
        url = '%s?rev=%s' % (urljoin(self._dburl, doc_id), quote(rev))
        response = yield from aiohttp.request(
            'DELETE', url,
            headers={
                'Accept': 'application/json'
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    def all(self, **options):
        response = yield from aiohttp.request(
            'GET', urljoin(self._dburl, '_all_docs'),
            headers={
                'Accept': 'application/json'
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    def put_design_doc(self, ddoc_name, ddoc, **options):
        posturl = urljoin(self._dburl, "_design/%s/" % ddoc_name)
        response = yield from aiohttp.request(
            'PUT', posturl, data=json_dumps(ddoc),
            headers={
                'Accept': 'application/json',
                'content-type': 'application/json'
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    def get_design_doc(self, ddoc_name, **options):
        posturl = urljoin(self._dburl, "_design/%s/" % ddoc_name)
        response = yield from aiohttp.request(
            'GET', posturl,
            headers={
                'Accept': 'application/json',
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    def delete_design_doc(self, ddoc_name, rev=None, **options):
        if rev == None:
            rev = yield from self.get_design_doc(ddoc_name)
            rev = rev._rev
        posturl = urljoin(self._dburl, "_design/%s/" % ddoc_name)
        url = '%s?rev=%s' % (posturl, quote(rev))
        response = yield from aiohttp.request(
            'DELETE', url,
            headers={
                'Accept': 'application/json'
            })
        data = yield from response.read()
        return Bunch(**json_loads(data))

    def view(self, ddoc_name, view, **options):
        if not options:
            options = {}
        
        options.setdefault('reduce', options.setdefault('group', False))
        viewurl = urljoin(
            self._dburl, "_design/%s/_view/%s" % (ddoc_name, view))

        for option in options:
            options[option] = json.dumps(options[option])

        query = urlencode(options)
        viewurl = "%s?%s" % (viewurl, query)
        self.logger.debug('GET: %s', viewurl)
        response = yield from aiohttp.request(
            'GET', viewurl,
            headers={
                'Accept': 'application/json',
            })
        data = yield from response.read()
        return ResultList(**self.check_errors(json_loads(data)))

    def check_errors(self, data):
        if 'error' in data:
            raise CouchDBError(data['reason'])
        return data
