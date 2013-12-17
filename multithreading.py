import os
import socket
import signal
import time
import logging
import tulip
import tulip.http
from tulip.http import websocket
import threading
import time
import tulip
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
init_modules=['watchdog', 'Observer', 'FileSystemEventHandler']

class MyStreamProtocol(tulip.StreamProtocol):
    def connection_lost(self, exc):
        self.transport = None

        if exc is not None:
            self.set_exception(exc)
        else:
            if not self._parser_buffer or self._parser_buffer._waiter._state != tulip.futures._PENDING:
                return
            self.feed_eof()
            
debugging = True
def set_debug(isdebug):
    global debugging
    debugging = isdebug

class ChildProcess:

    def __init__(self, up_read, down_write, args, sock, protocol_factory, ssl):
        self.up_read = up_read
        self.down_write = down_write
        self.args = args
        self.sock = sock
        self.protocol_factory = protocol_factory
        self.ssl = ssl
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        # start server
        self.loop = loop = tulip.new_event_loop()
        tulip.set_event_loop(loop)

        def stop():
            self.loop.stop()
            os._exit(0)
        loop.add_signal_handler(signal.SIGINT, stop)

        f = loop.start_serving(
            self.protocol_factory, sock=self.sock, ssl=self.ssl)
        x = loop.run_until_complete(f)[0]
        self.logger.info('Starting srv worker process {} on {}'.format(
            os.getpid(), x.getsockname()))

        # heartbeat
        self.heartbeat()

        tulip.get_event_loop().run_forever()
        os._exit(0)

    @tulip.task
    def heartbeat(self):
        # setup pipes
        read_transport, read_proto = yield from self.loop.connect_read_pipe(
            MyStreamProtocol, os.fdopen(self.up_read, 'rb'))
        write_transport, _ = yield from self.loop.connect_write_pipe(
            MyStreamProtocol, os.fdopen(self.down_write, 'wb'))

        reader = read_proto.set_parser(websocket.WebSocketParser())
        writer = websocket.WebSocketWriter(write_transport)

        while True:
            msg = yield from reader.read()
            if msg is None:
                self.logger.info('Superviser is dead, {} stopping...'.format(os.getpid()))
                self.loop.stop()
                break
            elif msg.tp == websocket.MSG_PING:
                writer.pong()
            elif msg.tp == websocket.MSG_CLOSE:
                self.logger.debug("Got close message, quitting")
                self.loop.stop()
                break

        read_transport.close()
        write_transport.close()


class Worker:

    _started = False

    def __init__(self, loop, args, sock, protocol_factory, ssl):
        self.loop = loop
        self.args = args
        self.sock = sock
        self.protocol_factory = protocol_factory
        self.ssl = ssl
        self.shutdown = False
        self.restart = False
        self.start()
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self):
        assert not self._started
        self._started = True

        up_read, up_write = os.pipe()
        down_read, down_write = os.pipe()
        args, sock = self.args, self.sock

        pid = os.fork()
        if pid:
            # parent
            os.close(up_read)
            os.close(down_write)
            self.connect(pid, up_write, down_read)
        else:
            # child
            os.close(up_write)
            os.close(down_read)

            # cleanup after fork
            tulip.set_event_loop(None)

            # setup process
            process = ChildProcess(up_read, down_write, args, sock,
                                   self.protocol_factory, self.ssl)
            process.start()

    @tulip.task
    def heartbeat(self, writer):
        global debugging
        while True:
            yield from tulip.sleep(15)
            if self.shutdown or self.restart:
                self.logger.info(
                    'Restarting/Shutting worker process: {}'.format(self.pid))
                writer.close()
                self.kill()
                if self.restart:
                    self.start()
                self.restart = False
                return

            if (time.monotonic() - self.ping) < 30:
                writer.ping()
            elif not debugging:
                print(debugging)
                self.logger.info(
                    'Restart unresponsive worker process: {}'.format(self.pid))
                self.kill()
                self.start()
                return

    @tulip.task
    def chat(self, reader, proto):
        while True:
            msg = yield from reader.read()
            if msg is None or self.restart or self.shutdown:
                self.logger.info(
                    'Restart worker process: {}'.format(self.pid))
                reader.close()
                self.kill()
                self.restart = False
                if not self.shutdown:
                    self.start()
                self.shutdown = False
                return
            elif msg.tp == websocket.MSG_PONG:
                self.ping = time.monotonic()

    @tulip.task
    def connect(self, pid, up_write, down_read):
        # setup pipes
        read_transport, proto = yield from self.loop.connect_read_pipe(
            MyStreamProtocol, os.fdopen(down_read, 'rb'))
        write_transport, _ = yield from self.loop.connect_write_pipe(
            MyStreamProtocol, os.fdopen(up_write, 'wb'))

        # websocket protocol
        reader = proto.set_parser(websocket.WebSocketParser())
        writer = websocket.WebSocketWriter(write_transport)

        # store info
        self.pid = pid
        self.ping = time.monotonic()
        self.rtransport = read_transport
        self.wtransport = write_transport
        self.chat_task = self.chat(reader, proto)
        self.heartbeat_task = self.heartbeat(writer)

    def kill(self):
        self._started = False
        self.chat_task.cancel()
        self.heartbeat_task.cancel()
        self.rtransport.close()
        self.wtransport.close()
        os.kill(self.pid, signal.SIGTERM)

    def reload_modules(self):
        import sys
        if 'init_modules' in globals():
            global init_modules
            curdir = os.getcwd()
            for key, module in list(sys.modules.items()):
                if hasattr(module,'__file__'):
                    if os.path.commonprefix([module.__file__, curdir]) == curdir:
                        print("reloading:", key)
                        del(sys.modules[key])
                else:
                    pass
                    #print(module)
        else:
            init_modules = sys.modules.keys()


class Superviser:

    def __init__(self, args):
        self.loop = tulip.get_event_loop()
        self.args = args
        self.workers = []
        self.logger = logging.getLogger(self.__class__.__name__)

    def start(self, protocol_factory, ssl):
        # bind socket
        sock = self.sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.args.host, self.args.port))
        sock.listen(1024)
        sock.setblocking(False)

        # start processes
        for idx in range(self.args.workers):
            self.workers.append(
                Worker(self.loop, self.args, sock, protocol_factory, ssl))

        results = []

        def reload_worker_modules(module_path):
            protocol_factory.reload_handlers(module_path)
            #for worker in self.workers:
            #    worker.reload_modules()

        class ReloadingEventHandler(FileSystemEventHandler):
            def __init__(self, loop):
                super(ReloadingEventHandler, self).__init__()
                self.loop = loop
            def on_modified(self, event):
                src_path = event.src_path.decode('utf8')
                basename = os.path.basename(src_path)
                if basename.endswith('py') and \
                   not basename.startswith('.') and\
                   not basename.startswith('flycheck'):
                    self.loop.call_soon_threadsafe(reload_worker_modules, src_path)
                    #self.loop.call_soon_threadsafe(kill_workers)

        reload_handler = ReloadingEventHandler(self.loop)
        observer = Observer()
        observer.schedule(reload_handler, path='.', recursive=True)
        observer.start()

        def kill_workers(shutdown=False):
            for worker in self.workers:
                worker.shutdown = shutdown
                worker.restart = True
                if shutdown:
                    pass
                    #self.loop.stop()

        def kill_server():
            observer.stop()
            observer.join()
            running = False
            kill_workers(True)
            self.loop.stop()
            self.logger.debug("Exiting")
            exit(0)

        self.loop.add_signal_handler(signal.SIGINT, kill_server)
        self.loop.add_signal_handler(signal.SIGTERM, kill_workers)
        self.loop.run_forever()
