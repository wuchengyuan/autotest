# -*- coding: utf-8 -*-

"""
公共模块
"""
import os
import re
import time
import functools
import logging
import hashlib
import configparser

global_var = dict()


def get_config():
    """
    读取配置文件
    :return: 配置文件信息
    """
    cfg = {}
    config = configparser.ConfigParser()
    config_file = get_project_path() + "config.ini"
    config.read(config_file, encoding='utf8')
    sections = config.sections()
    if not sections:
        logging.error(u'读取配置文件失败')
    for section in sections:
        cfg[section] = {}
        options = config.options(section)
        for option in options:
            cfg[section][option] = config.get(section, option)
    return cfg


def set_config(section, option, value=None):
    config = configparser.ConfigParser()
    config_file = get_project_path() + "config.ini"
    config.read(config_file)
    config.set(section, option, value)
    with open(config_file, 'w') as f:
        config.write(f)


def get_project_path():
    """
    获取代码根路径
    :return: 代码根路径
    """
    src_path = os.path.dirname(__file__)
    return re.split('auto_utils', src_path)[0]


def time_statistics(func):
    """
    装饰函数，计算步骤执行时间
    :param func:
    :return:
    """
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        start_time = time.time()
        f = func(*args, **kw)
        end_time = time.time()
        during_time = end_time - start_time
        logging.info(u'%s操作耗时：%s秒' % (func.__name__, during_time))
        if during_time > 5:
            logging.warning(u'%s操作耗时大于5S，性能需要优化！'
                            % func.__name__)
        return f
    return _wrapper


def get_now():
    """
    获取当前时间
    :return: 当前时间
    """
    return time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())


def check_list(str_type):
    """
    检查参数是否为list类型
    :param str_type: id='aa'/['id=aa',...]
    :return: true: 是list类型 false: 不是list类型
    """
    return isinstance(str_type, list)


def log_on():
    level = get_config().get('project_config').get('logging')
    log_path = get_project_path() + 'result/'
    if not os.path.isdir(log_path):
        os.mkdir(log_path)
    log_name = log_path + 'logging.log'
    logging.basicConfig(level=level,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=log_name,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter('%(asctime)s %(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def md5_encryption(msg):
        m2 = hashlib.md5()
        m2.update(msg.encode('utf8'))
        return m2.hexdigest()
