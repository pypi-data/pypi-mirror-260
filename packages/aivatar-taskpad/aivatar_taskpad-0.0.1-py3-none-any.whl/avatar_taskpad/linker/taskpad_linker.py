# -*- coding: utf-8 -*-

from arthub_login_widgets import LoginBackend
import json
import os

from avatar_taskpad.command.command_handler import CommandNames
from avatar_taskpad.dcc_executor import DCCExecutor
from avatar_taskpad.logger import get_logger
from avatar_taskpad.observer import Observer
from avatar_taskpad.utils.constants import TASKPAD_SERVER_PORT
from avatar_taskpad.utils.ipc import IPCServer

class TaskpadLinker(Observer):
    def __init__(self, dcc_executor):
        # init dcc executor
        self.__dcc_executor = dcc_executor if type(dcc_executor) == DCCExecutor else DCCExecutor()

        # init logger
        self.logger = get_logger()

        # init ipc
        self.ipc = IPCServer()
        self.listen_port = self.ipc.init(TASKPAD_SERVER_PORT)
        self.logger.info("TaskpadLinker listen port: {0}".format(self.listen_port))

        # init account backend
        self.backend = LoginBackend(terminal_type="dcc", business_type="default", dev_mode=False)
        self.taskpad_window = None

    def __del__(self):
        self.close()

    def set_receive_callback(self, callback = None):
        self.ipc.set_receive_callback(callback)

    def pull_up_peer(self):
        if self.ipc.is_connected() or self.taskpad_window is not None:
            return
        
        if not self.backend.is_login():
            if not self.backend.popup_login():
                self.logger.warning("login failed, user canceled.")
                return

        self.taskpad_window = self.backend.popup_task_pad(self.listen_port)

    def close(self):
        self.ipc.close()
        self.close_peer()

    def close_peer(self):
        if self.taskpad_window:
            self.taskpad_window.close()
            self.taskpad_window = None

    def on_event(self, event):
        if event.event_type == CommandNames.GetPlatfromName.value:
            return self.get_platform_name(event.data)
        if event.event_type == CommandNames.UploadReviewFile.value:
            return self.upload_record_video(event.data)
        if event.event_type == CommandNames.OpenFileInDCC.value:
            return self.open_file_in_dcc(event.data)
        if event.event_type == CommandNames.SaveFileInDCC.value:
            return self.save_file_in_dcc(event.data)
        return None

    def get_platform_name(self, _):
        """
        data: {}

        resposne: {
            "result": 0,
            "message": "get platfrom info success",
            "platfrom": "mobu"
        }
        """
        platfrom_name = self.__dcc_executor.get_platform()
        b_success = (platfrom_name == DCCExecutor.UNKNOWN_PLATFORM)
        self.logger.info("execute get platform command, result {0}, platform {1}".format(b_success, platfrom_name))
        resposne = {
            "result": 0 if b_success else -1,
            "message": "get platfrom info success" if b_success else "unknown platform",
            "platfrom": platfrom_name
        }
        return json.dumps(resposne).encode('utf-8')
    
    def upload_record_video(self, data):
        """
        data: {
            "filepath": "c:/user/video/xxx-xxx-xxxx.mp4"
        }

        response: {
            "command": "upload_record_video",
            "filepath": "c:/user/video/xxx-xxx-xxxx.mp4"
        }
        """
        filepath = data['filepath']
        self.logger.info("upload video {0} to taskpad..".format(filepath))

        # send upload video request to taskpad
        request = {
            "command": "upload_record_video",
            "filepath": filepath
        }
        self.ipc.send_message(json.dumps(request).encode('utf-8'))

        # send response to capturer
        response = {
            "package": "response",
            "command": "upload_record_video",
            "filepath": filepath
        }
        return json.dumps(response).encode('utf-8')

    def open_file_in_dcc(self, data):
        """
        data: {
            "filepath": "g:/test/test1.fbx"
        }

        response: {
            "command": "open_file_response",
            "result": 0,
            "message": "Open file in dcc successfully."
        }
        """
        try:
            filepath = data['filepath']
            if not os.path.exists(filepath):
                raise FileNotFoundError("Can't find the specified file {0}.".format(filepath))
            self.logger.info("open file {0} in dcc..".format(filepath))
            self.__dcc_executor.open_file(filepath, data, callback=self.on_file_opened_in_dcc)
        except ValueError:
            return json.dumps({
                "command": "open_file_response",
                "result": -1,
                "message": "Open file in dcc failed, missing filepath in request."
            }).encode('utf-8')
        except FileNotFoundError:
            return json.dumps({
                "command": "open_file_response",
                "result": -1,
                "message": "Open file in dcc failed, can't find the specified file {0}.".format(filepath)
            }).encode('utf-8')
        return None
    
    def on_file_opened_in_dcc(self, b_success, message):
        self.logger.info("open file in dcc finished, result={0} message={1}".format(b_success, message))
        response = {
            "command": "open_file_response",
            "result": 0 if b_success else -1,
            "message": message
        }
        self.ipc.send_message(json.dumps(response).encode('utf-8'))

    def save_file_in_dcc(self, _):
        """
        data: { }

        response: {
            "command": "save_file_response",
            "result": 0,
            "message": "Save file in dcc successfully.",
            "filepath": "g:/test/test1.fbx"
        }
        """
        self.logger.info("save file in dcc..")
        self.__dcc_executor.save_file(callback=self.on_file_saved_in_dcc)
        return None
    
    def on_file_saved_in_dcc(self, b_success, message, filepath):
        self.logger.info("save file in dcc finished, result={0} message={1} filepath={2}".format(b_success, message, filepath))
        response = {
            "command": "save_file_response",
            "result": 0 if b_success else -1,
            "message": message,
            "filepath": filepath
        }
        self.ipc.send_message(json.dumps(response).encode('utf-8'))
