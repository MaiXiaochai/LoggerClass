# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : logger.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/11/23 13:50
--------------------------------------
"""
from os import makedirs
from os.path import basename, exists
from logging.handlers import RotatingFileHandler
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO


class Logger:
    """ 封装的用于类的通用功能"""

    def __init__(self, log_dir: str = None, filename: str = None, max_size: float = None, backup_count: int = None):
        """
        :param log_dir:         保存日志的目录
        :param filename:        日志名称
        :param max_size:        单个日志文件最大大小，单位 MB
        :param backup_count:    除正名称为filename的文件外, 备份日志的数量
        """
        # 处理参数值
        self.log_dir = log_dir or '.'
        self.filename = filename or __name__
        max_size = max_size or 10
        self.max_size = max_size * 1024 ** 2
        self.backup_count = backup_count or 10

        # 一些默认的设置
        self.encoding = "utf-8"
        self.log_level = DEBUG
        self.file_log_level = INFO
        self.print_level = DEBUG
        self.formatter = "[ %(asctime)s ][ %(levelname)s ][ %(filename)s:%(funcName)s ][ %(message)s ]"

        # 处理 log 文件保存目录的路径
        self.log_dir = self.__format_path(log_dir)
        self.log_file_path = "{}{}".format(log_dir, filename)

        # log_dir 目录，如果不存在则创建
        self.__check_dirs(log_dir)

    def __get_logger(self):
        formatter = Formatter(self.formatter)

        rotating_file_handler = RotatingFileHandler(
            filename=self.log_file_path,
            maxBytes=self.max_size,
            backupCount=self.backup_count,
            encoding=self.encoding
        )

        # ≥ INFO级别才记录到文件
        rotating_file_handler.setLevel(self.file_log_level)
        rotating_file_handler.setFormatter(formatter)

        stream_handler = StreamHandler()

        # ≥ INFO级别才记录到文件
        stream_handler.setLevel(self.print_level)
        stream_handler.setFormatter(formatter)

        logger = getLogger(basename(__file__))
        logger.setLevel(self.log_level)

        logger.addHandler(stream_handler)
        logger.addHandler(rotating_file_handler)

        return logger

    @staticmethod
    def __format_path(dir_path: str) -> str:
        """主要功能
            1）'\' --> '/'
            2) 保证路径以'/'结尾
        """
        dir_path = dir_path.replace("\\", '/') if "\\" in dir_path else dir_path
        dir_path = dir_path if dir_path.endswith("/") else dir_path + '/'

        return dir_path

    @staticmethod
    def __check_dirs(dir_path: str):
        """检查目录是否存在，不存在则递归创建"""
        if not exists(dir_path):
            makedirs(dir_path)

    @property
    def log(self):
        return self.__get_logger()
