#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser  # 读取配置文件的包
import os
import logging
os.system('chcp 65001')
config = configparser.ConfigParser()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


def read_ini(ini_key):
    try:
        path = os.path.join(os.getcwd(), 'my_cfg.ini')
        config.read(path, encoding="utf-8")
        logging.debug(path)
        cfg_options = config.options(ini_key)  # 获取option
        return cfg_options
    except BaseException:
        logging.error('没有找到配置文件!!')
        path = os.path.join(os.getcwd(), 'cfg.ini')
        config.read(path, encoding="utf-8")
        logging.debug(path)
        cfg_options = config.options(ini_key)  # 获取option
        return cfg_options


