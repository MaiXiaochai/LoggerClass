# -*- coding: utf-8 -*-

"""
--------------------------------------
@File       : example.py
@Author     : maixiaochai
@Email      : maixiaochai@outlook.com
@CreatedOn  : 2020/11/23 15:26
--------------------------------------
"""

from logger import Logger


def demo():
    from time import sleep

    log = Logger().log
    print()
    for i in range(5):
        sleep(0.5)
        log.info(i)


if __name__ == '__main__':
    demo()
