# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 14:16
# @Author  : qxcnwu
# @FileName: InputObject.py
# @Software: PyCharm
import json
import os.path

from ScaleConvertionTools.CommonObject.MessageLogger import MessageLogger, Level


class InputObject:
    def __init__(self):
        self.vis_path = None
        self.nir_path = None
        self.save_path = None

        # 保存当前的结果
        self.vis_ans = None
        self.nir_ans = None
        self.ans = None

        self.vis_square = []
        self.nir_square = []

        self.ref = []

        self.message_box = []
        self.pic_show = []

        self.use_redis = False
        self.use_gpu = False
        self.use_show = False

        self.logger = None

    def check(self) -> bool:
        """
        检查
        :return:
        """
        mgl = MessageLogger()
        mgl.add_msg("Start check InputObject", Level.INFO)

        def check_exsis(path: str) -> bool:
            if path is None:
                return False
            return os.path.exists(path)

        if not check_exsis(self.vis_path):
            mgl.add_msg("No such vis picture path", Level.ERROR)
            return False

        if not check_exsis(self.nir_path):
            mgl.add_msg("No such nir picture path", Level.ERROR)
            return False

        if not check_exsis(self.save_path):
            mgl.add_msg("No such save dir", Level.ERROR)
            return False

        # 检查数量是否相同
        if len(self.ref) == len(self.vis_square) and len(self.vis_square) == len(self.nir_square):
            mgl.add_msg("Check InputObject Successful", Level.INFO)
            return True

        mgl.add_msg("wrong number of vis and nir square and refs", Level.ERROR)
        return False

    def save(self, path: str):
        """
        保存为json
        :param path:
        :return:
        """
        dic = self.__dict__
        dic["logger"] = None
        with open(path, "w") as fd:
            fd.write(json.dumps(dic))
            fd.close()
        return

    @staticmethod
    def load(path: str):
        """
        导入json
        :param path:
        :return:
        """
        with open(path, "r") as fd:
            dic = json.loads(fd.read())
        fd.close()
        inobj = InputObject()
        for t in dic.keys():
            inobj.__setattr__(t, dic[t])
        return inobj