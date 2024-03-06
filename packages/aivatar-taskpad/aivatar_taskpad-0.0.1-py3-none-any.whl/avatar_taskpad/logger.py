# -*- coding: utf-8 -*-

import logging
import os
import sys

from .utils.filesystem import user_path

def get_logger():
    logger = logging.getLogger(__package__)
    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)

        # file handler
        log_path = os.path.join(user_path(), __package__ + "_log.txt")
        print("logger path: ", log_path)
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # console handler
        logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger
