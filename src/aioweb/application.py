#!/usr/bin/env python3
"""Simple server written using an event loop."""

import sys
assert sys.version >= '3.3', 'Please use Python 3.3 or higher.'
import argparse
import logging
import os
import sys
try:
    import ssl
except ImportError:  # pragma: no cover
    ssl = None
import asyncio
from aiohttp.server import ServerHttpProtocol
from .multithreading import Superviser
from debug import set_except_hook


ARGS = argparse.ArgumentParser(description="Run simple http server.")
ARGS.add_argument(
    '--host', action="store", dest='host',
    default='127.0.0.1', help='Host name')
ARGS.add_argument(
    '--port', action="store", dest='port',
    default=9999, type=int, help='Port number')
ARGS.add_argument(
    '--iocp', action="store_true", dest='iocp', help='Windows IOCP event loop')
ARGS.add_argument(
    '--ssl', action="store_true", dest='ssl', help='Run ssl mode.')
ARGS.add_argument(
    '--sslcert', action="store", dest='certfile', help='SSL cert file.')
ARGS.add_argument(
    '--sslkey', action="store", dest='keyfile', help='SSL key file.')
ARGS.add_argument(
    '--workers', action="store", dest='workers',
    default=1, type=int, help='Number of workers.')
ARGS.add_argument(
    '--staticroot', action="store", dest='staticroot',
    default='./static/', type=str, help='Static root.')
ARGS.add_argument(
    '--jsroot', action="store", dest='jsroot',
    default='./js/', type=str, help='Js root.')


def configure_logging():
    #logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logging.getLogger().level = logging.DEBUG
    logging.getLogger('asyncio').level = logging.ERROR


class ProtocolFactory(ServerHttpProtocol):
    def __call__(self):
        raise NotImplemented()

    def reload_handlers(self, module_path=None):
        self.router.reload_handlers(module_path)


def main(protocol_factory=None):
    configure_logging()
    if not protocol_factory:
        protocol_factory = ProtocolFactory()
    set_except_hook()
    args = ARGS.parse_args()

    if ':' in args.host:
        args.host, port = args.host.split(':', 1)
        args.port = int(port)

    if args.iocp:
        from asyncio import windows_events
        sys.argv.remove('--iocp')
        logging.info('using iocp')
        el = windows_events.ProactorEventLoop()
        asyncio.set_event_loop(el)

    if args.ssl:
        here = os.path.join(os.path.dirname(__file__), 'tests')

        if args.certfile:
            certfile = args.certfile or os.path.join(here, 'sample.crt')
            keyfile = args.keyfile or os.path.join(here, 'sample.key')
        else:
            certfile = os.path.join(here, 'sample.crt')
            keyfile = os.path.join(here, 'sample.key')

        sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        sslcontext.load_cert_chain(certfile, keyfile)
    else:
        sslcontext = None

    superviser = Superviser(args)
    superviser.start(protocol_factory, sslcontext)


if __name__ == '__main__':
    main()
