# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 23:39
# @Author  : qxcnwu
# @FileName: PictureProcess.py
# @Software: PyCharm

import cv2
import numpy as np
from PIL import Image

from ScaleConvertionTools.CommonObject.Build import logger
from ScaleConvertionTools.CommonObject.InputObject import InputObject
from ScaleConvertionTools.CommonObject.MessageLogger import MessageLogger
from ScaleConvertionTools.CommonObject.TmpFile import Tmp


class Vis_Process:
    def __init__(self, inObj: InputObject):
        self.inObj = inObj
        self.small_img = []
        self.small_array = np.zeros((224, 224, 3))
        self.msg = MessageLogger()

        self.make_small()
        self.make_big()

    @logger
    def make_small(self):
        """
        裁剪
        :return:
        """
        # 裁剪
        img = cv2.imread(self.inObj.vis_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        array = np.array(img)
        for square in self.inObj.vis_square:
            self.small_img.append(np.array(
                Image.fromarray(
                    array[int(square[0]):int(square[2]), int(square[1]):int(square[3])].astype(np.uint8)).resize(
                    (56, 56))))
        # 拼接
        for i in range(4):
            for j in range(4):
                self.small_array[56 * i:56 * i + 56, j * 56:j * 56 + 56, :] = self.small_img[
                    (i * 4 + j) % len(self.small_img)]
        Image.fromarray(self.small_array.astype(np.uint8)).save(Tmp.vis_path_small_name)
        return

    @logger
    def make_big(self):
        """
        裁剪
        :return:
        """
        # 裁剪
        img = cv2.imread(self.inObj.vis_path)
        img = cv2.resize(img, (224, 224))
        # 拼接
        cv2.imwrite(Tmp.vis_path_big_name, img)
        return


class Nir_Process:
    def __init__(self, inObj: InputObject):
        self.inObj = inObj
        self.small_img = []
        self.small_array = np.zeros((224, 224, 3))
        self.msg = MessageLogger()

        self.make_small()
        self.make_big()

    @logger
    def make_small(self):
        """
        裁剪
        :return:
        """
        # 裁剪
        img = cv2.imread(self.inObj.nir_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        array = np.array(img)
        dat = array.astype(np.uint8)

        if len(array.shape) < 3:
            dat = np.expand_dims(dat, axis=2)
            array = np.concatenate([dat, dat, dat], axis=2)
        else:
            array = dat
        for square in self.inObj.nir_square:
            self.small_img.append(np.array(
                Image.fromarray(
                    array[int(square[0]):int(square[2]), int(square[1]):int(square[3])].astype(np.uint8)).resize(
                    (56, 56))))
        # 拼接
        for i in range(4):
            for j in range(4):
                self.small_array[56 * i:56 * i + 56, j * 56:j * 56 + 56, :] = self.small_img[
                    (i * 4 + j) % len(self.small_img)]
        Image.fromarray(self.small_array.astype(np.uint8)).save(Tmp.nir_path_small_name)
        return

    @logger
    def make_big(self):
        """
        裁剪
        :return:
        """
        # 裁剪
        img = cv2.imread(self.inObj.nir_path)
        img = cv2.resize(img.astype(np.uint8), (224, 224))
        # 拼接
        cv2.imwrite(Tmp.nir_path_big_name, img)
        return
