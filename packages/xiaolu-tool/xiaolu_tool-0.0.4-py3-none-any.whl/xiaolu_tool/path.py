import inspect
import sys
from xiaolu_tool.commonKit import get_all_folders_in_directory
import os


def get_root_path():
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    dirname = os.path.dirname(file_path)
    while dirname != '/':
        directory = get_all_folders_in_directory(dirname)
        if 'venv' in directory:
            break
        dirname = os.path.dirname(dirname)
    return dirname


def get_log_path(root_path):
    file_path = root_path + "/logs"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path


def get_output_path(root_path):
    file_path = root_path + "/output"
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    return file_path


class ProjectPath:
    ROOT_PATH = get_root_path()
    RESOURCES_PATH = ROOT_PATH + "/resource"
    LOG_PATH = get_log_path(ROOT_PATH)
    OUTPUT_PATH = get_output_path(ROOT_PATH)
    CONF_PATH = RESOURCES_PATH + "/conf.ini"
    DB_CONFIG_PATH = RESOURCES_PATH + "/db.ini"
    THRIFT_CONFIG_PATH = RESOURCES_PATH + "/thrift.ini"



