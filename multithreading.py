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
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler


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
            tulip.StreamProtocol, os.fdopen(self.up_read, 'rb'))
        write_transport, _ = yield from self.loop.connect_write_pipe(
            tulip.StreamProtocol, os.fdopen(self.down_write, 'wb'))

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
        while True:
            yield from tulip.sleep(15)
            if not self.shutdown:
                writer.close()
                self.kill()
                return

            if (time.monotonic() - self.ping) < 30:
                writer.ping()
            else:
                self.logger.info(
                    'Restart unresponsive worker process: {}'.format(self.pid))
                self.kill()
                self.start()
                return

    @tulip.task
    def chat(self, reader):
        while True:
            msg = yield from reader.read()
            if not self.shutdown:
                self.kill()
                return
            if msg is None:
                self.logger.info(
                    'Restart unresponsive worker process: {}'.format(self.pid))
                self.kill()
                self.start()
                return
            elif msg.tp == websocket.MSG_PONG:
                self.ping = time.monotonic()

    @tulip.task
    def connect(self, pid, up_write, down_read):
        # setup pipes
        read_transport, proto = yield from self.loop.connect_read_pipe(
            tulip.StreamProtocol, os.fdopen(down_read, 'rb'))
        write_transport, _ = yield from self.loop.connect_write_pipe(
            tulip.StreamProtocol, os.fdopen(up_write, 'wb'))

        # websocket protocol
        reader = proto.set_parser(websocket.WebSocketParser())
        writer = websocket.WebSocketWriter(write_transport)

        # store info
        self.pid = pid
        self.ping = time.monotonic()
        self.rtransport = read_transport
        self.wtransport = write_transport
        self.chat_task = self.chat(reader)
        self.heartbeat_task = self.heartbeat(writer)

    def kill(self):
        self._started = False
        self.chat_task.cancel()
        self.heartbeat_task.cancel()
        self.rtransport.close()
        self.wtransport.close()
        os.kill(self.pid, signal.SIGTERM)


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

        event_handler = LoggingEventHandler()
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=True)
        observer.start()

        def kill_workers(shutdown=False):
            for worker in self.workers:
                worker.shutdown = shutdown
                worker.kill()
                self.logger.debug("Restarting")
                self.loop.stop()

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