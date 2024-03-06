# -*- coding: utf-8 -*-

from enum import Enum

from avatar_taskpad.observer import Event

class Command():
    def execute(self, observable, data):
        raise NotImplementedError('Command.execute() is not implemented')

class CommandNames(Enum):
    # Taskpad commands
    GetPlatfromName = "get_platform_info"
    OpenFileInDCC = "open_file"
    SaveFileInDCC = "save_file"
    UploadReviewFile = "upload_review_file"

    # Capturer commands
    OpenCapturer = "open_capturer"
    RecordAborted = "record_aborted"

class GeneralCommand(Command):
    def __init__(self, name):
        self.__name = name

    def execute(self, observable, data):
        return observable.notify(Event(self.__name, data))

class CommandFactory:
    """
    Factory class for creating commands.
    :param name: Name of the command.
    :return command: Command object.
    :raises ValueError: Invalid command name.
    """
    @staticmethod
    def create_command(name):
        if name in {
            CommandNames.GetPlatfromName.value,
            CommandNames.OpenFileInDCC.value,
            CommandNames.SaveFileInDCC.value,
            CommandNames.UploadReviewFile.value,
            CommandNames.OpenCapturer.value,
            CommandNames.RecordAborted.value
            }:
            return GeneralCommand(name)
        else:
            raise ValueError("Invalid command name: {0}".format(name))
