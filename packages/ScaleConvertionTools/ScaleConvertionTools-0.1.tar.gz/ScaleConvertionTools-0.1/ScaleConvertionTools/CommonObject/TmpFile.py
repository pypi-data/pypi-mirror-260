# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 19:27
# @Author  : qxcnwu
# @FileName: TmpFile.py
# @Software: PyCharm
import os


class Tmp:
    plot_ref_path_name = "ref.jpg"
    vis_path_name = "vis.png"
    nir_path_name = "nir.png"
    vis_path_big_name = "vis_big.png"
    vis_path_small_name = "vis_small.png"
    nir_path_big_name = "nir_big.png"
    nir_path_small_name = "nir_small.png"

    @staticmethod
    def clear():
        for i in Tmp.__dict__.values():
            if os.path.exists(str(i)):
                os.remove(str(i))
        return
