# -*- coding: utf-8 -*-

import json

from .command_handler import CommandFactory
from avatar_taskpad.logger import get_logger
from avatar_taskpad.observer import Observable

class CommandParser(Observable):
    """
    Processes an incoming request and returns response.
    :param message: The incoming message
    :return response: The response, return None if no response is needed.
    """
    def process_request(self, message):
        logger = get_logger()
        try:
            # decode request
            data = json.loads(message.decode('utf-8'))

            # create command
            command_name = data['command']
            command = CommandFactory.create_command(command_name)

            # execute command
            logger.info("execute command {0}".format(command_name))
            response_data = command.execute(self, data)
            logger.info("repsonse: {0}".format(response_data))
            
            return response_data
        except json.decoder.JSONDecodeError:
            logger.error("Invalid JSON format:" + str(message))
            return
        except (ValueError, KeyError):
            logger.warning("Command or Params not found in the received message")
            return
