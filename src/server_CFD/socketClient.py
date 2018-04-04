
from tornado import escape
from tornado import gen
from tornado import httpclient
from tornado import httputil
from tornado import ioloop
from tornado import websocket

from collections import deque

import threading

import json

APPLICATION_JSON = 'application/json'

DEFAULT_CONNECT_TIMEOUT = 60
DEFAULT_REQUEST_TIMEOUT = 60


class WebSocketClient(object):

    def __init__(self,*, connect_timeout=DEFAULT_CONNECT_TIMEOUT,
                 request_timeout=DEFAULT_REQUEST_TIMEOUT):

        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout

    def connect(self, url):
        """Connect to the server.
        :param str url: server URL.
        """

        self._ioloop = ioloop.IOLoop()
        headers = httputil.HTTPHeaders({'Content-Type': APPLICATION_JSON})
        request = httpclient.HTTPRequest(url=url,
                                         connect_timeout=self.connect_timeout,
                                         request_timeout=self.request_timeout,
                                         headers=headers)

        self.ws_conn = websocket.WebSocketClientConnection(self._ioloop,
                                                           request)

        self._ioloop.add_future(self.ws_conn.connect_future, self._connect_callback)

    def _connect_callback(self, future):
        if future.exception() is None:
            self._ws_connection = future.result()
            self._on_connection_success()
            self._read_messages()
        else:
            self._on_connection_error(future.exception())

    def send(self, data):
        if not self._ws_connection:
            raise RuntimeError('Web socket connection is closed.')

        self._ws_connection.write_message(escape.utf8(json.dumps(data)))

    def close(self, future):
        """Close connection.
        """

        if not self._ws_connection:
            raise RuntimeError('Web socket connection is already closed.')

        self._ws_connection.close()

    @gen.coroutine
    def _read_messages(self):
        while True:
            msg = yield self._ws_connection.read_message()
            if msg is None:
                self._on_connection_close()
                break

            self._on_message(msg)

    def _on_message(self, msg):
        """This is called when new message is available from the server.
        :param str msg: server message.
        """
        print('Receiving', msg)
        pass

    def _on_connection_success(self):
        """This is called on successful connection ot the server.
        """

        pass

    def _on_connection_close(self):
        """This is called when server closed the connection.
        """
        pass

    def _on_connection_error(self, exception):
        """This is called in case if connection to the server could
        not established.
        """

        pass


class UsefulWebSocket1(WebSocketClient):
    def __init__(self, url):
        self.url = url
        self.data_deque = deque()
        super(UsefulWebSocket1, self).__init__()

    def connect(self):
        print(self.url)
        super(UsefulWebSocket1, self).connect(self.url)
        self._ioloop_thread = threading.Thread(target=self._run_ioloop)
        self._ioloop_thread.start()

    def _on_message(self, msg):
        print(msg)

    def send(self, data):
        self.data_deque.append(data)
        self._ioloop.add_future(self.ws_conn.connect_future, self._send)

    def _send(self, future):
        super(UsefulWebSocket1, self).send(self.data_deque.popleft())

    def _run_ioloop(self):
        self._ioloop.start()
        print('stop loop')

    def _stop_ioloop(self, future):
        self._ioloop.add_callback(self._ioloop.stop)

    def close(self):
        self._ioloop.add_future(self.ws_conn.connect_future, super(UsefulWebSocket1, self).close)
        self._ioloop.add_future(self.ws_conn.connect_future, self._stop_ioloop)

    def _on_connection_close(self):
        print('Connection Closed')

    def _on_connection_success(self):
        print('Connection Open')

    def _on_connection_error(self, exception):
        print('Connection closed due to: ', exception)


class UsefulWebSocket(object):
    def __init__(self, url, receiver):
        self.url = url
        self.receiver = receiver

    def send(self, data):
        ws = UsefulWebSocket1(self.url)
        ws.connect()
        ws.send({'receiver': self.receiver, 'algorithm': self.algorithm, 'method': data})
        ws.close()

    def resend(self, data):
        ws = UsefulWebSocket1(self.url)
        ws.connect()
        ws.send(data)
        ws.close()

class SocketModel3D(UsefulWebSocket):
    def __init__(self, url):
        super(SocketModel3D, self).__init__(url, 'model3D')


class SocketCFD(UsefulWebSocket):
    def __init__(self, url):
        super(SocketCFD, self).__init__(url, 'CFD')


class SocketDesign(UsefulWebSocket):
    def __init__(self, url):
        super(SocketDesign, self).__init__(url, 'design')


class SocketHandler(UsefulWebSocket):
    def __init__(self, url):
        super(SocketHandler, self).__init__(url, 'handler')