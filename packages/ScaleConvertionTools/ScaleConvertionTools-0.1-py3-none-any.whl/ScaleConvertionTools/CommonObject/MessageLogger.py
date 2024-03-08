# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 21:44
# @Author  : qxcnwu
# @FileName: MessageLogger.py
# @Software: PyCharm
from abc import abstractmethod


class Level:
    ERROR = 3
    WARNING = 2
    INFO = 1
    DEBUG = 0


class Singleton(object):
    def __init__(self, cls):
        """
        单例模式
        :param cls:
        """
        self._cls = cls
        self._instance = {}

    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]


class MsgConnecter:
    def __init__(self, lev: int):
        pass

    @abstractmethod
    def add_msg(self, msg: str):
        pass

    @abstractmethod
    def msg_type(self, msg: str) -> str:
        pass


class MessageLogger:
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, *x):
        if len(x) == 2:
            self.MSG = {
                Level.ERROR: [],
                Level.WARNING: [],
                Level.INFO: [],
                Level.DEBUG: []
            }
            self.context = x[0]
            self.level = x[1]

    def __add_msg(self, msg: str, l: int):
        """
        记录消息
        :param msg:
        :param l:
        :return:
        """
        self.MSG[l].append(msg)
        return

    def add_msg(self, msg: str, l: int):
        """
        记录消息
        :param msg:
        :param l:
        :return:
        """
        if l >= self.level:
            self.context.add_msg(self.context.msg_type(msg))
        self.__add_msg(msg, l)
        return
