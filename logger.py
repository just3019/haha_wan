#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2018/7/20

@author: gongyuan
"""

import logging
from logging.handlers import RotatingFileHandler


class Logger():
    def __init__(self, path, clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        self.path = path
        self.clevel = clevel
        self.Flevel = Flevel
        # 设置CMD日志

    #         sh = logging.StreamHandler()
    #         sh.setFormatter(fmt)
    #         sh.setLevel(clevel)
    #         设置文件日志

    def debug(self, message):
        self.fh = RotatingFileHandler(self.path, maxBytes=5 * 1024 * 1024, backupCount=1, encoding="utf-8")
        self.fh.setFormatter(self.fmt)
        self.fh.setLevel(self.Flevel)
        #         self.logger.addHandler(sh)
        self.logger.addHandler(self.fh)
        self.logger.debug(message)
        self.logger.removeHandler(self.fh)

    def info(self, message):
        self.fh = RotatingFileHandler(self.path, maxBytes=5 * 1024 * 1024, backupCount=1, encoding="utf-8")
        self.fh.setFormatter(self.fmt)
        self.fh.setLevel(self.Flevel)
        #         self.logger.addHandler(sh)
        self.logger.addHandler(self.fh)
        self.logger.info(message)
        self.logger.removeHandler(self.fh)

    def war(self, message):
        self.fh = RotatingFileHandler(self.path, maxBytes=5 * 1024 * 1024, backupCount=1, encoding="utf-8")
        self.fh.setFormatter(self.fmt)
        self.fh.setLevel(self.Flevel)
        #         self.logger.addHandler(sh)
        self.logger.addHandler(self.fh)
        self.logger.warn(message)
        self.logger.removeHandler(self.fh)

    def error(self, message):
        self.fh = RotatingFileHandler(self.path, maxBytes=5 * 1024 * 1024, backupCount=1, encoding="utf-8")
        self.fh.setFormatter(self.fmt)
        self.fh.setLevel(self.Flevel)
        #         self.logger.addHandler(sh)
        self.logger.addHandler(self.fh)
        self.logger.error(message)
        self.logger.removeHandler(self.fh)

    def cri(self, message):
        self.fh = RotatingFileHandler(self.path, maxBytes=5 * 1024 * 1024, backupCount=1, encoding="utf-8")
        self.fh.setFormatter(self.fmt)
        self.fh.setLevel(self.Flevel)
        #         self.logger.addHandler(sh)
        self.logger.addHandler(self.fh)
        self.logger.critical(message)
        self.logger.removeHandler(self.fh)


if __name__ == '__main__':
    logyyx = Logger('yyx.log', logging.ERROR, logging.DEBUG)
    logyyx.debug('一个debug信息')
    logyyx.info('一个info信息')
    logyyx.war('一个warning信息')
    logyyx.error('一个error信息')
    logyyx.cri('一个致命critical信息')
