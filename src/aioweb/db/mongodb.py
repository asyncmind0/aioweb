import logging
import asyncio
from .database import DatabaseAdapter
from pymongo.mongo_client import MongoClient


def _run_in_executor(method):
    """ Run the method in a executor, uses deault executor settings
    """
    def run(self, *args):
        loop = asyncio.get_event_loop()
        res = yield from loop.run_in_executor(None, method, self, *args)
        return res
    return run


class MongoDBAdapter(DatabaseAdapter):
    def __init__(self, url, dbname):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client = MongoClient()
        self.db = getattr(self.client, dbname)

    @_run_in_executor
    def info(self):
        return self.client.server_info()

    @_run_in_executor
    def put(self, document, doc_id=None, **options):
        collection = document.data['doc_type']
        collection = getattr(self.db, collection)
        if '_id' in document.data and document.data['_id']:
            _id = collection.update(document.data)
        else:
            if '_id' in document.data:
                del document.data['_id']
            _id = collection.insert(document.data)
        document.data['_id'] = _id
        return document

    @_run_in_executor
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

