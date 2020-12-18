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
from os.path import exists
from logging.handlers import RotatingFileHandler
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO


class Logger:
    """ 封装的用于类的通用功能"""

    def __init__(self, log_dir: str = None, filename: str = None, max_size: float = None, backup_count: int = None):
        """
        :param log_dir:         保存日志的目录
        :param filename:        日志名称，默认为 'test'
        :param max_size:        单个日志文件最大大小，单位 MB
        :param backup_count:    除正名称为filename的文件外, 备份日志的数量

        说明：
            1）默认只对级别 >= INFO 的日志才会进行log操作，可通过设置 self.log_level值来修改
            2）其它更多更进一步的设置， 请在 "log参数设置" 区进行设置
        """
        # ===========================[ 处理参数值 ]===========================
        log_dir = log_dir or '.'
        log_dir = self.__format_path(log_dir)

        filename = filename or 'test'
        self.filename = self.__check_log_suffix(filename)

        # log 文件绝对路径
        self.log_file_path = "{}{}".format(log_dir, self.filename)

        max_size = max_size or 256
        self.max_size = max_size * 1024 ** 2

        self.backup_count = backup_count or 4

        # ===========================[ log参数设置 ]===========================
        # 一些默认的设置
        self.encoding = "utf-8"

        # ≥ log_level 级别才会被log
        self.log_level = INFO

        # ≥ file_log_level 级别才会被记录到文件
        self.file_log_level = INFO

        # ≥ print_log_level 级别才会被打印到屏幕
        self.print_level = DEBUG

        self.formatter = "[ %(asctime)s ][ %(levelname)s ][ %(filename)s:%(funcName)s:%(lineno)d ][ %(message)s ]"

        # log_dir 目录，如果不存在则创建
        self.__check_dirs(log_dir)

    def __get_logger(self):
        formatter = Formatter(self.formatter)

        # log文件
        rotating_file_handler = RotatingFileHandler(
            filename=self.log_file_path,
            maxBytes=self.max_size,
            backupCount=self.backup_count,
            encoding=self.encoding
        )
        rotating_file_handler.setLevel(self.file_log_level)
        rotating_file_handler.setFormatter(formatter)

        # log print
        stream_handler = StreamHandler()
        stream_handler.setLevel(self.print_level)
        stream_handler.setFormatter(formatter)

        logger = getLogger()

        logger.setLevel(self.log_level)
        logger.addHandler(stream_handler)
        logger.addHandler(rotating_file_handler)

        return logger

    @staticmethod
    def __format_path(dir_path: str) -> str:
        """主要功能
            1）'\' --> '/'
            2) 保证dir_path以'/'结尾
        """
        dir_path = dir_path.replace("\\", '/') if "\\" in dir_path else dir_path
        dir_path = dir_path if dir_path.endswith("/") else dir_path + '/'

        return dir_path

    @staticmethod
    def __check_dirs(dir_path: str):
        """检查目录是否存在，不存在则递归创建"""
        if not exists(dir_path):
            makedirs(dir_path)

    @staticmethod
    def __check_log_suffix(log_name: str) -> str:
        """确保log_name是以'.log'"""
        suffix = '.log'

        if not log_name.endswith(suffix):
            log_name = f"{log_name}{suffix}"

        return log_name

    @property
    def log(self):
        return self.__get_logger()
