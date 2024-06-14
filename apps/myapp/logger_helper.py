#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import os
import sys

from myweb.settings import *


class LoggerSetup:
    def __init__(self, filename, log_dir):
        self.filename = filename
        self.log_dir = log_dir
        self.logger = self._setup_logger()

    def _setup_logger(self):
        # 创建日志目录（如果不存在）
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        log_file_path = os.path.join(self.log_dir, self.filename)

        # 创建日志记录器
        logger = logging.getLogger(self.filename)
        logger.setLevel(logging.INFO)

        # 如果记录器已经有处理器，先移除避免重复
        if not logger.handlers:
            # 创建文件处理器并设置级别为INFO
            fh = logging.FileHandler(log_file_path, 'a', encoding='utf-8')
            fh.setLevel(logging.INFO)

            # 创建格式化器并将其添加到处理器
            # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            # 添加处理器到记录器
            logger.addHandler(fh)

            # 也将日志输出到 Celery worker 的标准输出
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.INFO)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

        return logger

    def get_logger(self):
        return self.logger

    def redirect_std_output(self):
        sys.stdout = LoggerWriter(self.logger, logging.INFO)
        sys.stderr = LoggerWriter(self.logger, logging.ERROR)


class LoggerWriter:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.buffer = ""

    def write(self, message):
        if message != '\n':
            self.buffer += message
        if message.endswith('\n'):
            self.logger.log(self.level, self.buffer.rstrip())
            self.buffer = ""

    def flush(self):
        if self.buffer:
            self.logger.log(self.level, self.buffer.rstrip())
        self.buffer = ""