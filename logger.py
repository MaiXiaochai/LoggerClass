# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : logger.py
@Author     : maixiaochai
@CreatedOn  : 2020/11/23
@modified   : 2026/05/24
--------------------------------------
"""
import inspect
import threading
from logging import getLogger, StreamHandler, Formatter, INFO
from logging.handlers import RotatingFileHandler
from os import makedirs
from os.path import exists, join as path_join, dirname, basename


class Logger:
    """封装的用于类的通用日志功能"""

    _instance_counter = 0

    def __init__(
            self,
            log_dir: str = None,
            filename: str = None,
            max_size: float | int = None,
            backup_count: int = None):
        """
        :param log_dir:     保存日志的目录，默认在调用方文件同级 logs/ 目录下
        :param filename:    日志名称，默认使用调用方文件名.log
        :param max_size:    单个日志文件最大大小，单位 MB
        :param backup_count: 除名称为 filename 的文件外, 备份日志的数量

        说明：
            1）默认只对级别 >= INFO 的日志才会进行log操作，可通过设置 self.log_level 值来修改
            2）其它更多更进一步的设置，请在 "log参数设置" 区进行设置
        """
        # 获取调用方的文件信息
        caller_frame = inspect.stack()[1]
        caller_file = caller_frame.filename
        self._caller_module = caller_frame.frame.f_globals.get('__name__', '')

        # 确保每个实例有唯一标识
        Logger._instance_counter += 1
        self._instance_id = Logger._instance_counter

        # ===========================[ 处理参数值 ]===========================
        log_dir = log_dir or path_join(dirname(caller_file), 'logs')

        filename = filename or basename(caller_file)
        self.filename = self.__check_log_suffix(filename)

        # log 文件绝对路径
        self.log_file_path = path_join(log_dir, self.filename)

        max_size = max_size or 64
        self.max_size = max_size * 1024 ** 2

        self.backup_count = backup_count or 8

        # ===========================[ log参数设置 ]===========================
        self.encoding = "utf-8"
        self.log_level = INFO
        self.file_log_level = INFO
        self.print_level = INFO
        self.formatter = "[ %(asctime)s ][ %(levelname)s ][ %(message)s ]"

        # log_dir 目录，如果不存在则创建
        self.__check_dirs(log_dir)

        # 线程安全
        self._lock = threading.Lock()
        self._logger = None

    def __get_logger(self):
        if self._logger is None:
            with self._lock:
                if self._logger is None:
                    formatter = Formatter(self.formatter)

                    # 使用命名 logger 避免干扰根 logger
                    logger = getLogger(f"{self._caller_module}.Logger.{self._instance_id}")
                    logger.setLevel(self.log_level)

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

                    logger.addHandler(stream_handler)
                    logger.addHandler(rotating_file_handler)

                    self._logger = logger

        return self._logger

    @staticmethod
    def __check_dirs(dir_path: str):
        """检查目录是否存在，不存在则递归创建"""
        if not exists(dir_path):
            makedirs(dir_path)

    @staticmethod
    def __check_log_suffix(log_name: str) -> str:
        """确保log_name以'.log'结尾"""
        suffix = '.log'
        if not log_name.endswith(suffix):
            log_name = f"{log_name}{suffix}"
        return log_name

    @property
    def log(self):
        return self.__get_logger()
