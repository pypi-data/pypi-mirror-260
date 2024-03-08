# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 19:33
# @Author  : qxcnwu
# @FileName: SedProcess.py
# @Software: PyCharm
import numpy as np
import pandas as pd

from ScaleConvertionTools.CommonObject.Build import logger
from ScaleConvertionTools.CommonObject.InputObject import InputObject


class Sed_Process:
    def __init__(self, inObj: InputObject):
        """

        :param inObj:
        """
        self.inObj = inObj
        self.wave = []
        self.ref = []
        # 解析
        self.process()

    @logger
    def process(self):
        """
        处理
        :return:
        """
        for path in self.inObj.ref:
            self.wave, ref = decode_sed(path)
            self.ref.append(ref)
        return


def decode_sed(path: str) -> np.array:
    """
    导入xlsx文件
    :param path:
    :return:
    """
    if path.endswith("xls") or path.endswith("xlsx"):
        dat = pd.read_excel(path)
    else:
        dat = pd.read_csv()
    dat = np.array(dat)
    return dat[:, 0], dat[:, 1]
