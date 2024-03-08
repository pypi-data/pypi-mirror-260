# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 22:14
# @Author  : qxcnwu
# @FileName: MessageBoxes.py
# @Software: PyCharm
import time

from PyQt5.QtWidgets import QTextBrowser

from ScaleConvertionTools.CommonObject.MessageLogger import MsgConnecter, Level


class MessageBoxes(MsgConnecter):
    def __init__(self, msg_box: QTextBrowser, level: int = Level.DEBUG):
        super().__init__(level)
        self.msg_box = msg_box

    def add_msg(self, msg: str):
        """
        添加
        :param msg:
        :return:
        """
        self.msg_box.append(msg + "\n")

    def msg_type(self, msg: str) -> str:
        """
        格式
        :param msg:
        :return:
        """
        return "[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] " + msg
