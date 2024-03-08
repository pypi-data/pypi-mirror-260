# -*- coding: utf-8 -*-
# @Time    : 2024/3/6 11:05
# @Author  : qxcnwu
# @FileName: ProcessMain.py
# @Software: PyCharm

from ScaleConvertionTools.CommonObject.InputObject import InputObject
from ScaleConvertionTools.CommonObject.TmpFile import Tmp
from ScaleConvertionTools.DataProcess.AnswerSave import AnswerSave
from ScaleConvertionTools.DataProcess.PictureProcess import Vis_Process, Nir_Process
from ScaleConvertionTools.DataProcess.ResTransformerPredict import Predict
from ScaleConvertionTools.DataProcess.SedProcess import Sed_Process


def Process(inObj: InputObject):
    """
    处理
    :param inObj:
    :return:
    """
    Vis_Process(inObj)
    Nir_Process(inObj)
    sp = Sed_Process(inObj)
    pd = Predict(sp)
    AnswerSave(inObj, pd)
    Tmp.clear()
    return
