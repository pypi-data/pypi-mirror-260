# -*- coding: utf-8 -*-

from .command.command_parser import CommandParser
from .linker.capturer_linker import CapturerLinker
from .linker.taskpad_linker import TaskpadLinker
from .logger import get_logger

class AvatarTaskpad(object):
    def __init__(self, executor):
        self.__command_parser = CommandParser()
        self.__capturer_linker = None
        self.__taskpad_linker = None
        self.logger = get_logger()

        self.__init_capturer_linker()
        self.__init_taskpad_linker(executor)

    def __del__(self):
        self.logger.info("avatar taskpad closed")
        self.__taskpad_linker.close()

    @property
    def taskpad_listen_port(self):
        return self.__taskpad_linker.listen_port

    def OpenCapturer(self):
        self.__capturer_linker.pull_up_peer()

    def OpenTaskpad(self):
        self.__taskpad_linker.pull_up_peer()

    def CloseTaskpad(self):
        self.__taskpad_linker.close_peer()

    def __init_capturer_linker(self):
        self.__capturer_linker = CapturerLinker()
        self.__capturer_linker.set_receive_callback(self.__command_parser.process_request)
        self.__command_parser.register(self.__capturer_linker)

    def __init_taskpad_linker(self, executor):
        self.__taskpad_linker = TaskpadLinker(executor)
        self.__taskpad_linker.set_receive_callback(self.__command_parser.process_request)
        self.__command_parser.register(self.__taskpad_linker)
