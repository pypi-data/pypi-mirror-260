# -*- coding: utf-8 -*-

from abc import abstractmethod
from threading import Thread
import socket

from avatar_taskpad.observer import Observer
from avatar_taskpad.logger import get_logger
from avatar_taskpad.utils.ipc import IPCClient
from avatar_taskpad.utils.filesystem import is_process_exit, run_exe_nonblocking

class LinkerBase(Observer):
    def __init__(self):
        self.__ipc_client = IPCClient()
        self.logger = get_logger()

    def __del__(self):
        self.__ipc_client.close()
        self.__ipc_client = None

    @abstractmethod
    def get_peer_port(self):
        pass

    @abstractmethod
    def get_peer_name(self):
        pass

    @abstractmethod
    def get_peer_exe_path(self):
        pass

    @property
    def ipc_client(self):
        return self.__ipc_client

    def pull_up_peer(self):
        if self.__ipc_client and self.__ipc_client.is_connected():
            return

        if not is_process_exit(self.get_peer_name()):
            run_exe_nonblocking(self.get_peer_exe_path(), [])

        t_wait = Thread(target=self.__wait_until_peer_is_ready)
        t_wait.start()
        t_wait.join()

        self.__init_ipc_client()

    def set_receive_callback(self, callback = None):
        if self.__ipc_client is not None:
            self.__ipc_client.set_receive_callback(callback)

    def __wait_until_peer_is_ready(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while True:
            if self.__ipc_client is None:
                sock.close()
                return
            try:
                sock.connect(('127.0.0.1', self.get_peer_port()))
            except ConnectionRefusedError:
                self.logger.info("Waiting for peer at {0}...".format(self.get_peer_port()))
                continue

            self.logger.info("peer is ready!")
            break

        self.logger.info("close test socket: {0}".format(sock.getsockname()))
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    def __init_ipc_client(self):
        self.__ipc_client.init(self.get_peer_port())
