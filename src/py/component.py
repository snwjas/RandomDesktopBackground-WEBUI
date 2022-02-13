# -*-coding:utf-8-*-

"""
组件

@author Myles Yang
"""

import os
import sys
from threading import Timer


class SingletonMetaclass(type):
    """ 单例元类 """

    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super(SingletonMetaclass, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(SingletonMetaclass, cls).__call__(*args, **kwargs)
        return cls.__instance


class CustomLogger(object, metaclass=SingletonMetaclass):
    """ 自定义日志记录类 """
    from loguru import logger
    from loguru._logger import Logger
    logger.opt(lazy=True, colors=True)
    # 日志格式
    __log_format = '{time:YYYY-MM-DD HH:mm:ss,SSS} | {level}\t | {file}:{function}:{line} | {message}'
    # 日志类型定义
    LOGGING_DEBUG = 10
    LOGGING_INFO = 20
    LOGGING_WARNING = 30
    LOGGING_ERROR = 40
    LOGGING_CRITICAL = 50
    LOGURU_SUCCESS = 25

    def __init__(self, log_srcpath: str = ''):
        self.__log_srcpath = log_srcpath if log_srcpath else ''

    def __add_file_handler(self):
        handler_id = self.logger.add(
            sink=os.path.join(self.__log_srcpath, 'run.{time:YYYYMMDD}.log'),
            format=self.__log_format,
            rotation='1 day',
            retention=30,
            enqueue=True,
            encoding='UTF-8'
        )
        return handler_id

    def __add_console_handler(self):
        info_handler_id = self.logger.add(sink=sys.stdout,
                                          level=self.LOGGING_INFO,
                                          # fg #097D80
                                          format='<g>' + self.__log_format + '</>',
                                          colorize=True,
                                          filter=lambda record: record["level"].name == "INFO"
                                          )
        err_handler_id = self.logger.add(sink=sys.stdout,
                                         level=self.LOGGING_ERROR,
                                         # fg #F56C6C
                                         format='<r>' + self.__log_format + '</>',
                                         colorize=True,
                                         filter=lambda record: record["level"].name == "ERROR"
                                         )
        return info_handler_id, err_handler_id

    def use_file_console_logger(self) -> Logger:
        self.logger.remove(handler_id=None)
        self.__add_file_handler()
        self.__add_console_handler()
        return self.logger

    def use_console_logger(self) -> Logger:
        self.logger.remove(handler_id=None)
        self.__add_console_handler()
        return self.logger

    def use_file_logger(self) -> Logger:
        self.logger.remove(handler_id=None)
        self.__add_file_handler()
        return self.logger

    def user_none(self) -> Logger:
        self.logger.remove(handler_id=None)
        return self.logger

    def set_logpath(self, log_srcpath: str):
        log_srcpath = log_srcpath if log_srcpath else ''
        self.__log_srcpath = log_srcpath

    def get_logger(self) -> Logger:
        return self.logger


class SimpleTaskTimer(object):
    """
    简单的循环单任务定时器，非阻塞当前线程

    @author Myles Yang
    """

    def __init__(self):
        self.__timer: Timer = None
        self.__seconds = 0
        self.__action = None
        self.__args = None
        self.__kwargs = None

    def run(self, seconds: int, action, args=None, kwargs=None):
        """
        执行循环定时任务

        :param seconds: 任务执行间隔，单位秒
        :param action: 任务函数
        :param args: 函数参数
        """
        if not callable(action):
            raise AttributeError("参数action非法，请传入函数变量")

        if self.is_running():
            return

        self.__action = action
        self.__seconds = seconds
        self.__args = args if args is not None else []
        self.__kwargs = kwargs if kwargs is not None else {}

        self.__run_action()

    def __run_action(self):
        self.__timer = Timer(self.__seconds, self.__hook, self.__args, self.__kwargs)
        self.__timer.start()

    def __hook(self, *args, **kwargs):
        self.__action(*args, **kwargs)
        self.__run_action()

    def is_running(self) -> bool:
        """
        判断任务是否在执行
        """
        return self.__timer and self.__timer.is_alive()

    def cancel(self):
        """
        取消循环定时任务
        """
        if self.is_running():
            self.__timer.cancel()
            self.__timer = None


class AppBreathe(object):
    """
    定义App心跳行为，用于检测客户端是否仍然在连接（客户端循环请求发送心跳请求）：
        定时器 __seconds 检测一次，连续 __times 次没接收到心跳请求则判定客户端失去连接

    @author Myles Yang
    """

    def __init__(self, interval: int = 60, times: int = 5):
        """
        :param interval: 循环计时器间隔，单位秒
        :param times: 循环检测次数
        """
        self.__timer: SimpleTaskTimer = None
        # 定时器循环频率
        self.__seconds: int = interval
        # 检测次数
        self.__times: int = times
        # 记录没有收到心跳信号次数
        self.__signals: int = 0

    def __action(self, callback):
        self.__signals += 1
        if self.__signals > self.__times:
            if callback and callable(callback):
                callback()

    def run(self, callback=None):
        """
        启动
        :param callback: 判定为失去连接时发生的回调
        """
        if self.__timer:
            return
        self.__timer = SimpleTaskTimer()
        self.__timer.run(self.__seconds, self.__action, [callback])

    def is_alive(self) -> bool:
        """ 客户端连接是否仍存活 """
        return self.__signals <= self.__times

    def record_alive(self):
        """ 重置信号 """
        self.__signals = 0
        return True
