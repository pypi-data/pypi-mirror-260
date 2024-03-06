# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import absolute_import

import logging
import os
import socket
import sys
from threading import Thread

def get_user_path():
    return os.path.expanduser("~")

class IPCSocket(object):
    k_receive_buffer_size = 10240

    def __init__(self):
        self.socket = None
        self.logger = self.__get_logger()
        self.__receive_callback = None

    def __del__(self):
        self.close()

    def set_receive_callback(self, callback = None):
        self.__receive_callback = callback

    """
        Send message to peer
        :param msg(bytes): message to send
    """
    def send_message(self, msg):
        if self.socket is None:
            self.logger.error("Failed to send message because socket is not connected")
            return

        self.logger.info('send message: {0}'.format(str(msg)))
        self.socket.sendall(msg)

    def close(self):
        if self.socket is not None:
            self.socket.shutdown(socket.SHUT_RDWR)
            self.socket.close()
            self.socket = None

    def read_data(self):
        if self.socket is None:
            return
        self.logger.info("start listen for data {0}".format(self.socket.getpeername()))
        self.socket.settimeout(None)
        while True:
            recv_data = bytes()
            while True:
                try:
                    data = self.socket.recv(IPCSocket.k_receive_buffer_size)
                    if len(data) == 0:
                        self.logger.warning("recv data is empty, connection closed! {0}".format(self.socket.getpeername()))
                        raise socket.error
                except (AttributeError, OSError, socket.error):
                    self.logger.warning("connection peer closed")
                    if self.socket is not None:
                        self.socket.shutdown(socket.SHUT_RDWR)
                        self.socket.close()
                        self.socket = None

                if self.socket is None:
                    return

                recv_data += data
                if len(data) < IPCSocket.k_receive_buffer_size:
                    break

            self.logger.info(recv_data)
            if self.__receive_callback is not None:
                response = self.__receive_callback(recv_data)
                if response is not None:
                    self.send_message(response)

    def is_connected(self):
        if self.socket is None:
            return False
        try:
            self.socket.getpeername()
        except socket.error:
            return False
        return True

    def __get_logger(self):
        class_name = self.__class__.__name__
        logger = logging.getLogger(class_name)
        if len(logger.handlers) == 0:
            logger.setLevel(logging.DEBUG)

            # file handler
            # log_path = os.path.join(get_user_path(), class_name + "_log.txt")
            # print("logger path: ", log_path)
            # file_handler = logging.FileHandler(log_path)
            # file_handler.setLevel(logging.DEBUG)
            # formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            # file_handler.setFormatter(formatter)
            # logger.addHandler(file_handler)

            # console handler
            logger.addHandler(logging.StreamHandler(sys.stdout))
        return logger

class IPCServer(IPCSocket):
    def __init__(self):
        super(IPCServer, self).__init__()

        self.__listen_socket = None
        self.__accept_thread = None

    def init(self, listen_port = 0):
        listen_port = self.__socket_bind(listen_port)
        return listen_port
    
    def close(self):
        super(IPCServer, self).close()
        if self.__listen_socket is not None:
            try:
                self.__listen_socket.shutdown(socket.SHUT_RDWR)
                self.__listen_socket.close()
            except socket.error:
                pass
            self.__listen_socket = None

    def __socket_bind(self, listen_port):
        if self.__listen_socket is None:
            self.__listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__listen_socket.bind(('127.0.0.1', listen_port))
            self.__listen_socket.listen(5)
            self.__listen_socket.settimeout(1)

            # create accept thread
            if self.__accept_thread is None:
                self.__accept_thread = Thread(target=self.__accept_client)
                self.__accept_thread.start()
        bind_port = self.__listen_socket.getsockname()[1]
        return bind_port

    def __accept_client(self):
        while True:
            try:
                if self.__listen_socket is None:
                    break
                client, addr = self.__listen_socket.accept()
                self.logger.info("client connected: {0}".format(addr))
            except socket.timeout:
                continue
            except OSError as e:
                self.logger.info("listen socket closed")
                return

            if self.socket is not None:
                try:
                    self.logger.warning("only one client can connect, close the old one: {0}".format(self.socket.getpeername()))
                    self.socket.shutdown(socket.SHUT_RDWR)
                    self.socket.close()
                except OSError:
                    # socket has been shutdown
                    pass
                finally:
                    self.socket = None

            self.socket = client
            t = Thread(target=self.read_data)
            t.start()

class IPCClient(IPCSocket):
    def init(self, server_port):
        return self.__socket_connect(server_port)

    def __socket_connect(self, server_port):
        if self.socket is not None:
            self.logger.warning("socket has been connected")
            return False

        self.logger.info("connect server : {0}".format(server_port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(('127.0.0.1', server_port))
        except socket.error as e:
            self.logger.exception("connect failed: failed to connect to server")
            self.socket = None
            return False

        # create read thread
        t = Thread(target=self.read_data)
        t.start()
        self.logger.info("connect localhost:{0} successfully, client addr is {1}".format(server_port, self.socket.getsockname()))
        return True
