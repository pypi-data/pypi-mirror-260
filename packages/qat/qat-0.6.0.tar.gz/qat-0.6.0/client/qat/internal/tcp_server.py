# -*- coding: utf-8 -*-
# (c) Copyright 2023, Qat’s Authors

"""
A simple TCP server
"""

from threading import Lock, Thread

import json
import socketserver

from qat.internal.qt_custom_object import QtCustomObject

callbacks_lock = Lock()
callbacks = {}


class QatRequestHandler(socketserver.StreamRequestHandler):
    """
    Request handler derived from StreamRequestHandler
    """
    def handle(self):
        print(f'New connection from {self.client_address[0]}')
        while True:
            try:
                header = self.rfile.readline().strip()
            except ConnectionResetError:
                break
            except: # pylint: disable=bare-except
                print('Error reading connected socket')
                break
            if header == b'':
                print('Connection was closed by the client')
                break

            try:
                length = int(header)
                content = self.rfile.read(length).decode('utf-8')
                self.execute_callback(json.loads(content))
            except Exception as error: # pylint: disable=broad-exception-caught
                # Avoid stopping the server upon errors
                print('Error in request handler: ' + str(error))


    def execute_callback(self, content: dict):
        """
        Execute the callback 
        """
        # Avoid cyclic import
        # pylint: disable = import-outside-toplevel
        # pylint: disable = cyclic-import
        from qat.internal.qt_object import QtObject
        callback_id = content['id']
        with callbacks_lock:
            if callback_id in callbacks:
                callback_elements = callbacks[callback_id]
                context = callback_elements[0]
                callback = callback_elements[1]
            else:
                print(f"Unknown callback ID: {callback_id}")
                return

        if 'args' in content:
            arg = content['args']
            if 'value' in arg:
                value = arg['value']
                if isinstance(value, dict):
                    callback(QtCustomObject(value))
                else:
                    callback(value)
            elif 'object' in arg:
                callback(QtObject(context, arg['object']))

        else:
            callback()


class TcpServer():
    """
    Class implementing a TCP server
    """
    daemon_threads = True

    def __init__(self, context, host="127.0.0.1", port=None) -> None:
        """
        Constructor.
        """
        self._context = context
        self._host = host
        self._port = port
        self._server = None
        self._thread = None

    def start(self):
        """
        Start the server thread
        """
        self._server = socketserver.ThreadingTCPServer(
            (self._host, 0), QatRequestHandler)
        self._port = self._server.socket.getsockname()[1]
        self._thread = Thread(target=self._internal_serve, daemon=True)
        self._thread.start()

    def stop(self):
        """
        Stop the server thread
        """
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join()

    def _internal_serve(self):
        try:
            self._server.serve_forever()
        except Exception: # pylint: disable=broad-exception-caught
            # Avoid raising exceptions from threads
            pass

    def get_host(self) -> str:
        """
        Return the host address
        """
        return self._host

    def get_port(self) -> int:
        """
        Return the server port
        """
        return self._port

    def register_callback(self, callback_id, callback) -> int:
        """
        Register the given callback.
        """
        with callbacks_lock:
            callbacks[callback_id] = (self._context, callback)

        return callback_id

    def unregister_callback(self, callback_id):
        """
        Unregister the given callback
        """
        with callbacks_lock:
            if callback_id in callbacks:
                del callbacks[callback_id]
