# -*- coding: utf-8 -*-
# @Time    : 2024/3/6 0:25
# @Author  : qxcnwu
# @FileName: ResTransformerPredict.py
# @Software: PyCharm
from typing import List

import numpy as np
from ScaleConvertion.PicProcess.DataPredict import predict
from scipy.optimize import minimize

from ScaleConvertionTools.CommonObject.Build import logger
from ScaleConvertionTools.CommonObject.TmpFile import Tmp
from ScaleConvertionTools.DataProcess import SedProcess


class Predict:
    def __init__(self, sp: SedProcess):
        self.sp = sp
        self.ans = None
        self.ans_vis = None
        self.ans_nir = None
        self.index = None

        self.found_index()
        self.predict_vis()
        self.predict_nir()
        self.concate()

    @staticmethod
    def compute(ref: List[List[float]], ans: List[float]):
        """
        计算
        :param ref:
        :param ans:
        :return:
        """
        k = []
        for i in range(16):
            k.append(np.array(ref[i % len(ref)]) * ans[i])
        k = np.array(k)
        ans = np.mean(k, axis=0)
        return ans

    @logger
    def found_index(self):
        """
        查找大于700nm的第一个波段
        :return:
        """
        arr = np.array(self.sp.wave)
        self.index = np.where(arr >= 700)[0][0]
        return

    @logger
    def predict_vis(self):
        """
        可见光预测
        :return:
        """
        ans, err = predict(Tmp.vis_path_small_name, [Tmp.vis_path_big_name])
        self.ans_vis = Predict.compute(self.sp.ref, ans[0])
        return

    @logger
    def predict_nir(self):
        """
        近红外预测
        :return:
        """
        ans, err = predict(Tmp.nir_path_small_name, [Tmp.nir_path_big_name])
        self.ans_nir = Predict.compute(self.sp.ref, ans[0])
        return

    @logger
    def concate(self):
        """
        拼接部分融合
        :return:
        """
        sm = Smooth(self.ans_vis, self.ans_nir, self.index)
        self.ans = sm.ans
        return


class Smooth:
    def __init__(self, vis: np.array, nir: np.array, index: int, k: int = 40):
        self.vis = vis
        self.nir = nir
        self.START = int(index - k / 2)
        self.END = int(index + k - k / 2)

        self.tmp = vis
        self.tmp[index:] = nir[index:]
        self.old = self.tmp[self.START:self.END]

        self.k = k
        self.x = np.arange(-(k // 2), k // 2, 1)
        self.tmp = []
        self.lines = None

        self.ans = self.vis
        self.ans[:index] = vis[:index]
        self.ans[index:] = nir[index:]

        # 优化
        self.optimized()

    def mape(self, smoothed):
        """
        计算相对误差越小越好
        :param smoothed:
        :return:
        """
        return np.mean(np.abs(smoothed - self.old) / self.old)

    def line(self):
        array_rgb = np.linspace(0, 1, self.k)
        array_nir = 1 - array_rgb
        self.lines = self.vis[self.START:self.END] * array_nir + \
                     self.nir[self.START:self.END] * array_rgb
        return

    def loss_function(self, params):
        y = self.auto_smooth(params)
        a = 1 - np.corrcoef(y, self.old)[0, 1]
        b = 1 - np.corrcoef(y, self.lines)[0, 1]
        if params == 0.5:
            self.bias = a / b
        return a + b * self.bias

    def auto_smooth(self, a: float):
        """
        曲线平滑
        :param md:
        :return:
        """
        array_rgb = 1 - 1 / (1 + np.exp(-a * self.x))
        array_nir = 1 - array_rgb
        return self.vis[self.START:self.END] * array_nir + self.nir[self.START:self.END] * array_rgb

    def optimized(self):
        self.line()
        initial_params = 0.5  # 初始化参数
        result = minimize(self.loss_function, initial_params, method='Nelder-Mead', bounds=[(0, 2)])
        self.ans[self.START:self.END] = self.auto_smooth(result.x[0])
        return
