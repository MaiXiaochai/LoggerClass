# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : example.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/11/23 15:26
--------------------------------------
"""

from logging import WARNING
from logger import Logger


def demo_basic():
    """基本用法：默认参数，日志写入调用方同级 logs/ 目录"""
    log = Logger().log

    for i in range(3):
        log.info(f"基本用法测试: {i}")


def demo_custom():
    """自定义参数：指定日志目录和文件名"""
    log = Logger(
        log_dir="./test_logs",
        filename="my_app.log",
        max_size=1,       # 1MB
        backup_count=3
    ).log

    log.warning("自定义日志测试")
    log.error("错误日志测试")


def demo_level():
    """日志级别过滤：只输出 WARNING 及以上"""
    logger = Logger(filename="level_test")
    logger.print_level = WARNING  # 屏幕只显示 WARNING 及以上

    log = logger.log
    log.debug("这条 DEBUG 不会显示")
    log.info("这条 INFO 不会显示")
    log.warning("这条 WARNING 会显示")
    log.error("这条 ERROR 会显示")


def demo_thread_safe():
    """多线程安全测试"""
    import threading

    logger = Logger(filename="thread_test")

    def worker(name):
        log = logger.log
        for i in range(3):
            log.info(f"[{name}] 第 {i} 条日志")

    threads = [threading.Thread(target=worker, args=(f"线程-{i}",)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    import shutil
    import os

    # 清理之前的测试日志
    for d in ('logs', 'test_logs'):
        if os.path.exists(d):
            shutil.rmtree(d)

    print("=== 1) 基本用法 ===")
    demo_basic()

    print("\n=== 2) 自定义参数 ===")
    demo_custom()

    print("\n=== 3) 日志级别过滤 ===")
    demo_level()

    print("\n=== 4) 多线程安全 ===")
    demo_thread_safe()

    # 展示生成的文件
    print("\n=== 生成的日志文件 ===")
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.log'):
                path = os.path.join(root, f)
                print(f"\n📄 {path}:")
                with open(path) as fh:
                    print(fh.read(), end='')

    # 清理
    for d in ('logs', 'test_logs'):
        if os.path.exists(d):
            shutil.rmtree(d)
