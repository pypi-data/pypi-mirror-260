# -*- coding: utf-8 -*-
# @Time    : 2024/3/6 10:30
# @Author  : qxcnwu
# @FileName: AnswerSave.py
# @Software: PyCharm
import os
import time

import cv2
import matplotlib.pyplot as plt

from ScaleConvertionTools.CommonObject.Build import logger
from ScaleConvertionTools.CommonObject.InputObject import InputObject
from ScaleConvertionTools.DataProcess.ResTransformerPredict import Predict


class AnswerSave:
    def __init__(self, inObj: InputObject, pred: Predict):
        """
        保存结果
        :param inObj:
        :param pred:
        """
        self.name = str(time.time_ns())
        self.inObj = inObj
        self.pred = pred

        self.save_json()
        self.save_pic()

    @logger
    def save_json(self):
        """
        保存json格式的文件
        :return:
        """
        # 结果保存
        self.inObj.ans = self.pred.ans.tolist()
        self.inObj.vis_ans = self.pred.ans_vis.tolist()
        self.inObj.nir_ans = self.pred.ans_nir.tolist()

        self.inObj.save(os.path.join(self.inObj.save_path, self.name + ".json"))

        return

    @logger
    def save_pic(self):
        """
        保存图像
        :return:
        """
        for idx, ref in enumerate(self.pred.sp.ref):
            plt.plot(self.pred.sp.wave, ref, label=str(idx))
        plt.plot(self.pred.sp.wave, self.inObj.ans, label="sc", linestyle="--", color="black")
        plt.xlabel("wave length(nm)")
        plt.ylabel("ref")
        plt.legend()
        plt.subplots_adjust()
        plt.savefig(os.path.join(self.inObj.save_path, self.name + ".png"), dpi=600)
        plt.close()

        if self.inObj.use_show:
            img = cv2.imread(os.path.join(self.inObj.save_path, self.name + ".png"))
            # 显示图片，后面会讲解
            cv2.imshow("image", img)
            # 等待按键
            cv2.waitKey(0)
        return