from debug import pprint, shell, profile, debug as sj_debug
import logging
import aiohttp

class ErrorHandlerMixin():
    def _write_headers(self):
        headers = email.message.Message()
        response = aiohttp.Response(
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

        response.add_header('Content-type', 'text/html')
        response.send_headers()
        return response

    def handle_404(self, exception, message, args):
        logging.debug("404: %s", message.path)

    def handle_error(self, exception, message, request_args=None):
        """Default handler exception handler"""
        sj_debug() ###############################################################
        if isinstance(exception, aiohttp.errors.HttpStatusException):
            if hasattr(self, 'handle_%s' % exception.code):
                response = getattr(self, 'handle_%s' % exception.code)(
                    exception, message, request_args)
        if not response:
            response = self._write_headers()

        response.write(("Error: %s" % str(exception)).encode('utf-8'))
        return response