from debug import pprint, shell, profile, debug as sj_debug
import sys
import json
import tulip
import tulip.http
from urllib.parse import quote
from urllib.request import urljoin
from uuid import uuid4


class Bunch():
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        
    def __str__(self):
        return str(self.__dict__)


class DatabaseAdapter:
    pass


class CouchDBAdapter(DatabaseAdapter):
    def __init__(self, url, dbname=None):
        self._url = url
        self._dbname = dbname
        
    @property
    def _dburl(self):
        return urljoin(self._url, self._dbname + '/')
    
    def info(self, doc_id=None):
        url = self._dburl
        if doc_id:
            url = urljoin(url, doc_id)
        response = yield from tulip.http.request(
            'GET', url, 
            headers={
                'Accept':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)
        
    def create_db(self, dbname=None, **options):
        if not dbname:
            dbname = self._dbname
        response = yield from tulip.http.request(
            'PUT', urljoin(self._url, dbname), 
            headers={
                'Accept':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

    def delete_db(self, dbname=None, **options):
        if not dbname:
            dbname = self._dbname
        response = yield from tulip.http.request(
            'DELETE', urljoin(self._url, dbname), 
            headers={
                'Accept':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

        
    def put(self, document, doc_id=None, **options):
        if not isinstance(document, dict):
            document = document.__dict__
        document = {key: val for key, val in document.items() if not key.startswith('__')}
        if not doc_id:
            doc_id = document.get('_id', document.get('id'))
            if doc_id:
                del document['id']
        if not doc_id:
            doc_id = str(uuid4())
        posturl = urljoin(self._dburl, doc_id)
        response = yield from tulip.http.request(
            'POST', self._dburl, data=json.dumps(document), 
            headers={
                'Accept':'application/json',
                'content-type':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

    def get(self, doc_id, **options):
        response = yield from tulip.http.request(
            'GET', urljoin(self._dburl, doc_id),
            headers={
                'Accept':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

    def delete(self, doc_id, rev=None, **options):
        if rev == None:
            rev = yield from self.info(doc_id)
            rev = rev._rev
        url = '%s?rev=%s' % (urljoin(self._dburl, doc_id), quote(rev))
        response = yield from tulip.http.request(
            'DELETE', url,
            headers={
                'Accept':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)
            
    def all(self, **options):
        response = yield from tulip.http.request(
            'GET', urljoin(self._dburl, '_all_docs'),
            headers={
                'Accept':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

        
    def put_design_doc(self, ddoc_name, ddoc, **options):
        posturl = urljoin(self._dburl, "_design/%s/" % ddoc_name)
        response = yield from tulip.http.request(
            'PUT', posturl, data=json.dumps(ddoc), 
            headers={
                'Accept':'application/json',
                'content-type':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

    def get_design_doc(self, ddoc_name, **options):
        posturl = urljoin(self._dburl, "_design/%s/" % ddoc_name)
        response = yield from tulip.http.request(
            'GET', posturl,
            headers={
                'Accept':'application/json',
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

    def delete_design_doc(self, ddoc_name, rev=None, **options):
        if rev == None:
            rev = yield from self.get_design_doc(ddoc_name)
            rev = rev._rev
        posturl = urljoin(self._dburl, "_design/%s/" % ddoc_name)
        url = '%s?rev=%s' % (posturl, quote(rev))
        response = yield from tulip.http.request(
            'DELETE', url,
            headers={
                'Accept':'application/json'
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)

    def view(self, ddoc, view, **options):
        viewurl = urljoin(self._dburl, "_design/%s/_view/%s" % (ddoc, view))
        if options:
            query = urlencode(options)
            viewurl ="%s?%s" % (viewurl, query)
        response = yield from tulip.http.request(
            'GET', viewurl,
            headers={
                'Accept':'application/json',
            })
        data = yield from response.read(decode=True)
        return Bunch(**data)