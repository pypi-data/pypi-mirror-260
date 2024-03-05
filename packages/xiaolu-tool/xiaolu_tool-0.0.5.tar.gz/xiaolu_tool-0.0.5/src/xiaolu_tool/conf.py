import configparser
import path


def get_env():
    _conf_param = configparser.ConfigParser()
    _conf_param.read_file(open(path.ProjectPath.CONF_PATH))
    return _conf_param["env"]["env"]


def get_ding_param():
    _conf_param = configparser.ConfigParser()
    _conf_param.read_file(open(path.ProjectPath.CONF_PATH))
    return {'secret': _conf_param['env']['export_ding_secret'], 'webhook': _conf_param['env']['export_ding_webhook']}


def get_param(conf_file_name, conf_key):
    conf_params = configparser.ConfigParser()
    conf_params.read_file(open(path.ProjectPath.RESOURCES_PATH + f"/{conf_file_name}"))
    return conf_params[conf_key]
