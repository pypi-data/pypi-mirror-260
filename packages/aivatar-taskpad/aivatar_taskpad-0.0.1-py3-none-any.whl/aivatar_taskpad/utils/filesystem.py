# -*- coding: utf-8 -*-

from threading import Thread
import os
import subprocess

import avatar_taskpad
from .constants import CAPTURER_EXE_NAME

def is_process_exit(process_name):
    result = subprocess.run(["tasklist"], capture_output=True, text=True)
    return process_name in result.stdout

def get_module_path():
    return os.path.dirname(avatar_taskpad.__file__)

def user_path():
    return os.path.expanduser("~")

def get_capturer_exe_path():
    module_path = get_module_path()
    return os.path.join(module_path, "resources", "client", CAPTURER_EXE_NAME, CAPTURER_EXE_NAME + ".exe")

def is_capturer_running():
    return is_process_exit(CAPTURER_EXE_NAME + ".exe")

def run_exe(exe_path, args):
    if not os.path.exists(exe_path):
        return
    command = [exe_path] + args
    if (hasattr(subprocess, 'run')):
        subprocess.run(command, shell=True)
    else:
        subprocess.Popen(command, shell=True)

def run_exe_nonblocking(exe_path, args):
    t = Thread(target=run_exe, args=(exe_path, args))
    t.start()
