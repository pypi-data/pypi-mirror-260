import time
import os
from pathlib import Path
import requests
import pandas as pd
from log import LogFactory
logger = LogFactory.logger


def currentTimeStamp():
    """
    获取当前时间戳以ms为单位
    """
    return int(time.time() * 1000)


def get_files_in_directory(
    current_directory: str, join_dir_path=False, file_type=None, without_extension=False
):
    """
    获取当前目录下的文件，只获取文件不遍历子目录, join_dir_path为True代表要拼接完整路径，False只返回文件名集合。without_extension是否需要携带文件名后缀
    """
    # 获取当前目录下的所有文件和文件夹
    all_items = os.listdir(current_directory)

    # 过滤出当前目录下的文件（不包括子目录）
    if join_dir_path:
        files_in_current_directory = [
            os.path.join(current_directory, item)
            for item in all_items
            if os.path.isfile(os.path.join(current_directory, item))
            and (file_type is None or item.endswith(file_type))
        ]
    else:
        files_in_current_directory = [
            item
            for item in all_items
            if os.path.isfile(os.path.join(current_directory, item))
            and (file_type is None or item.endswith(file_type))
        ]
    if without_extension:
        return [Path(f).stem for f in files_in_current_directory]
    return files_in_current_directory


def get_all_folders_in_directory(directory, join_dir_path=False):
    """
    获取目录下的所有文件夹
    @join_dir_path 返回文件夹名是否需要目录前缀，默认不带全路径前缀
    """
    if join_dir_path:
        return [
            os.path.join(directory, folder)
            for folder in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, folder))
        ]
    return [
        folder
        for folder in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, folder))
    ]


def get_file_name(file, has_extension=False):
    """
    获取文件名不包含路径， has_extension是否需要携带后缀名，默认不带
     """
    file_name, extension = os.path.splitext(os.path.basename(file))
    if has_extension:
        return f"{file_name}{extension}"
    else:
        return file_name


def http_get(url, param=None, headers=None):
    if not url:
        raise ValueError("URL cannot be empty")
    if param and not isinstance(param, dict):
        raise ValueError("param must be a dictionary")
    if headers and not isinstance(headers, dict):
        raise ValueError("header parameter must be a dictionary")
    try:
        response = requests.get(url, params=param, headers=headers)
        if response.status_code == 200:
            logger.info(f"request {url} success response_data is {response.json()}")
            return response.json()
        else:
            logger.info(f"request {url} fail code is {response.status_code}")
    except requests.HTTPError as err:
        logger.info(f"request {url} fail: {err}")
    except Exception as err:
        logger.info(f"when request{url} An unexpected error occurred: {err}")


def http_post(url, headers=None, param_body=None, json_body=None):
    if not url:
        raise ValueError("URL cannot be empty")
    if headers and not isinstance(headers, dict):
        raise ValueError("headers parameter must be a dictionary")
    try:
        response = requests.post(url, headers=headers, json=json_body, data=param_body)
        if response.status_code == 200:
            logger.info(f"request {url} success response_data is {response.json()}")
            return response.json()
        else:
            logger.info(f"request {url} fail code is {response.status_code}")
    except requests.HTTPError as err:
        logger.error(f"request {url} fail: {err}")
    except Exception as err:
        logger.error(f"when request{url} An unexpected error occurred: {err}")


def to_dict(obj):
    if (
        isinstance(obj, str)
        or isinstance(obj, bool)
        or isinstance(obj, int)
        or isinstance(obj, float)
    ):
        return obj
    if isinstance(obj, (list, tuple)):
        return [to_dict(item) for item in obj]
    elif isinstance(obj, set):
        return {to_dict(item) for item in obj}
    elif isinstance(obj, dict):
        return {key: to_dict(value) for key, value in obj.items()}
    return {
        k: to_dict(attr)
        for k, attr in {
            k: getattr(obj, k)
            for k in dir(obj)
            if not callable(getattr(obj, k)) and not k.startswith("__")
        }.items()
        if attr is not None
    }



