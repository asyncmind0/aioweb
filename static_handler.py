import os
import tulip
import tulip.http
import email.message
from handler import Handler
import mimetypes
from router import Router
from config import config
from os.path import join, dirname


def get_routes(router=None):
    if not router:
        router = Router()
    router.add_handler(
        '/static/favicon.ico', StaticFileHandler(config['default']['staticroot']))
    router.add_handler('/dojo/', StaticFileHandler(
        join(dirname(__file__), 'static', 'dojo')))
    router.add_handler('/dijit/', StaticFileHandler(
        join(dirname(__file__), 'static', 'dojo')))
    router.add_handler(
        '/jasmine/', StaticFileHandler(join(dirname(__file__), 'static', 
                                            config['default']['jasmine']),
                                       baseurl='/jasmine/'))
    return router


class StaticFileHandler(Handler):
    def __init__(self, staticroot, baseurl='/'):
        super(StaticFileHandler, self).__init__(write_headers=False)
        self.staticroot = staticroot
        self.baseurl = baseurl

    def __call__(self, request_args=None):
        # path = message.path
        if request_args:
            request_args = request_args[0]

        path = self.request.path
        if path.startswith(self.baseurl):
            path = path[len(self.baseurl):]

        if (not path.isprintable() or '/.' in path):
            raise tulip.http.HttpStatusException(
                404, message="Bad path:%s" % path)
        else:
            filepath = path = os.path.join(self.staticroot, path)
            # self.logger.debug("staticroot:%s", os.path.join(self.staticroot,
            # path))
            if not os.path.exists(path):
                raise tulip.http.HttpStatusException(
                    404, message="Not found:%s" % path)
            else:
                isdir = os.path.isdir(path)

        headers = email.message.Message()
        for hdr, val in self.request.headers:
            headers.add_header(hdr, val)

        if isdir and not path.endswith('/'):
            path = path + '/'
            raise tulip.http.HttpStatusException(
                302, headers=(('URI', path), ('Location', path)))

        response = tulip.http.Response(
            self.server.transport, 200, close=True)
        response.add_header('Transfer-Encoding', 'chunked')

        # content encoding
        accept_encoding = headers.get('accept-encoding', '').lower()
        if 'deflate' in accept_encoding:
            response.add_header('Content-Encoding', 'deflate')
            response.add_compression_filter('deflate')
        elif 'gzip' in accept_encoding:
            response.add_header('Content-Encoding', 'gzip')
            response.add_compression_filter('gzip')

        response.add_chunking_filter(1025)

        if isdir:
            response.add_header('Content-type', 'text/html')
            response.send_headers()

            response.write(b'<ul>\r\n')
            for name in sorted(os.listdir(path)):
                if name.isprintable() and not name.startswith('.'):
                    try:
                        bname = name.encode('ascii')
                    except UnicodeError:
                        pass
                    else:
                        if os.path.isdir(os.path.join(path, name)):
                            response.write(b'<li><a href="' + bname +
                                           b'/">' + bname + b'/</a></li>\r\n')
                        else:
                            response.write(b'<li><a href="' + bname +
                                           b'">' + bname + b'</a></li>\r\n')
            response.write(b'</ul>')
        else:
            response.add_header('Content-type', mimetypes.guess_type(path)[0])
            response.send_headers()

            try:
                with open(path, 'rb') as fp:
                    chunk = fp.read(8196)
                    while chunk:
                        response.write(chunk)
                        chunk = fp.read(8196)
            except OSError:
                response.write(b'Cannot open')
        return response
