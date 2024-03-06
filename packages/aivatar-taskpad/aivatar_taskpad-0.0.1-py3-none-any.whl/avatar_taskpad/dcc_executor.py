# -*- coding: utf-8 -*-

"""
    Defines the interface for a Digital Content Creators (DCC) executor,
    these 
"""
class DCCExecutor(object):
    UNKNOWN_PLATFORM = "Unknown"

    """
        Open local file in dcc.
        :param filepath: Path to open
        :param data: Extra data
        :param callback: Callback function(result: bool, message: str)
    """
    def open_file(self, filepath, data, callback):
        callback(False, "open file not implement in dcc")

    """
        Save local file in dcc.
        :param filepath: Path to save
        :param callback: Callback function(result: bool, message: str, filepath: str)
    """
    def save_file(self, callback):
        callback(False, "save file not implement in dcc", None)

    """
        Return the name of the current DCC. e.g. motionbuilder, maya ...
        :return: str: Name of the current DCC
    """
    def get_platform(self):
        return DCCExecutor.UNKNOWN_PLATFORM
