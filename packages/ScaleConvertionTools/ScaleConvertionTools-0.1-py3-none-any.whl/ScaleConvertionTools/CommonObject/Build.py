# -*- coding: utf-8 -*-
# @Time    : 2024/3/6 0:07
# @Author  : qxcnwu
# @FileName: Build.py
# @Software: PyCharm
from ScaleConvertionTools.CommonObject.MessageLogger import MessageLogger, Level


def logger(func):
    """
    装饰器
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        msg = MessageLogger()
        # 运行函数
        try:
            msg.add_msg("Start " + str(func), Level.INFO)
            result = func(*args, **kwargs)
            msg.add_msg("Successful " + str(func), Level.INFO)
            return result
        except Exception as ex:
            msg.add_msg("Wrong " + str(func) + " type={},content={}".format(repr(ex), ex),
                        Level.ERROR)
            return False
    return wrapper
