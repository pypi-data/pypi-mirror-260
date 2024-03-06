# -*- coding: utf-8 -*-

import json

from .linker_base import LinkerBase
from avatar_taskpad.command.command_handler import CommandNames
from avatar_taskpad.utils.constants import CAPTURER_EXE_NAME, CAPTURER_SERVER_PORT
from avatar_taskpad.utils.filesystem import get_capturer_exe_path

class CapturerLinker(LinkerBase):
    def get_peer_port(self):
        return CAPTURER_SERVER_PORT
    
    def get_peer_name(self):
        return CAPTURER_EXE_NAME
    
    def get_peer_exe_path(self):
        return get_capturer_exe_path()

    def on_event(self, event):
        if event.event_type == CommandNames.OpenCapturer.value:
            return self.pull_up(event.data)
        if event.event_type == CommandNames.RecordAborted.value:
            return self.on_record_aborted(event.data)

        return None

    def pull_up(self, data):
        """
        data: {}

        response: {
            "result": 0,
            "message": "pull up capturer success"
        }
        """
        self.pull_up_peer()
        response = {
            "result": 0,
            "message": "pull up capturer success",
        }
        return json.dumps(response).encode('utf-8')
    
    def on_record_aborted(self, data):
        """
        data: {}

        response: {
            "package": "response",
            "command": "",
            "message": "receive abort message"
            "param": {}
        }
        """
        self.logger.info("on record aborted")
        response = {
            "package": "response",
            "command": "",
            "message": "receive abort message",
            "param": {}
        }
        return json.dumps(response).encode('utf-8')
