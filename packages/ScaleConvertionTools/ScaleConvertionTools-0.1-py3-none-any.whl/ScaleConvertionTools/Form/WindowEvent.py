# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 14:09
# @Author  : qxcnwu
# @FileName: WindowEvent.py
# @Software: PyCharm
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsView, QGraphicsPixmapItem
from qtpy import QtWidgets

from ScaleConvertionTools.CommonObject.InputObject import InputObject
from ScaleConvertionTools.CommonObject.MessageLogger import MessageLogger, Level
from ScaleConvertionTools.DataProcess.ProcessMain import Process
from ScaleConvertionTools.Form.MainWindow import Ui_MainWindow
from ScaleConvertionTools.Form.MessageBoxes import MessageBoxes


class EventInit:
    def __init__(self, win: Ui_MainWindow, inObj: InputObject):
        self.win = win
        self.inObj = inObj
        self.inObj.logger = MessageBoxes(self.win.textBrowser)
        # 创建对应的Logger日志
        MessageLogger(self.inObj.logger, Level.DEBUG)
        self.scale_vis_h = 1
        self.scale_vis_w = 1
        self.scale_nir_h = 1
        self.scale_nir_w = 1
        # 初始话点击按钮
        self.win.pushButton.clicked.connect(self.vis_button)
        self.win.pushButton_2.clicked.connect(self.nir_button)
        self.win.pushButton_3.clicked.connect(self.save_button)
        self.win.pushButton_4.clicked.connect(self.start_button)

    def vis_button(self):
        """
        点击上传近红外图像
        :return:
        """
        self.inObj.vis_path = QtWidgets.QFileDialog.getOpenFileName(None, "选取图像", "./",
                                                                    "Picture Files (*.png *.jpg *.tiff *.tif);;All Files (*)")[
            0]
        if self.inObj.vis_path is None:
            return
        self.win.lineEdit.setText(self.inObj.vis_path)
        self.qt_load_image(self.inObj.vis_path, self.win.graphicsView_2)
        return

    def nir_button(self):
        """
        点击上传可视化图像
        :return:
        """
        self.inObj.nir_path = QtWidgets.QFileDialog.getOpenFileName(None, "选取图像", "./",
                                                                    "Picture Files (*.png *.jpg *.tiff *.tif);;All Files (*)")[
            0]
        if self.inObj.nir_path is None:
            return
        self.win.lineEdit_2.setText(self.inObj.nir_path)
        self.qt_load_image(self.inObj.nir_path, self.win.graphicsView, False)
        return

    def save_button(self):
        """
        点击上传保存路径
        :return:
        """
        self.inObj.save_path = QtWidgets.QFileDialog.getExistingDirectory(None, "选取文件夹", "./")
        if self.inObj.save_path is None:
            return
        self.win.lineEdit_3.setText(self.inObj.save_path)
        return

    def start_button(self):
        """
        初始化执行
        :return:
        """

        def change_points(points, scale_w, scale_h):
            """
            改变点
            :return:
            """
            ans = []
            for point in points:
                ans.append([point[0] * scale_w, point[1] * scale_h, point[2] * scale_w, point[3] * scale_h])
            return ans

        def flue():
            # 填充可选项
            self.inObj.use_redis = self.win.checkBox.isChecked()
            self.inObj.use_gpu = self.win.checkBox_2.isChecked()
            self.inObj.use_show = self.win.checkBox_3.isChecked()
            # 填充可见光近红外位置
            self.inObj.vis_square = change_points(self.win.view2.temp_rect, self.scale_vis_w, self.scale_vis_h)
            self.inObj.nir_square = change_points(self.win.view3.temp_rect, self.scale_nir_w, self.scale_nir_h)
            # 填充对应的反射率曲线
            size = len(self.win.view3.sed) + len(self.win.view2.sed)
            self.inObj.ref = [i for i in range(size)]
            for i in self.win.view3.sed.keys():
                self.inObj.ref[i] = self.win.view3.sed[i]
            for i in self.win.view2.sed.keys():
                self.inObj.ref[i] = self.win.view2.sed[i]
            return

        def process():
            Process(self.inObj)
            return

        # 检查对应的文件是否完备当前需要生成对象
        flue()

        # 执行检查
        self.inObj.check()

        # 数据预处理
        Process(self.inObj)
        return

    def qt_load_image(self, image_path: str, graphicsView: QGraphicsView, isVis: bool = True):
        """
        导入图像
        :param image_path:
        :param graphicsView:
        :return:
        """
        size = graphicsView.geometry()
        img = cv2.imread(image_path)

        if isVis:
            self.scale_vis_w = img.shape[0] / size.width()
            self.scale_vis_h = img.shape[1] / size.height()
        else:
            self.scale_nir_w = img.shape[0] / size.width()
            self.scale_nir_h = img.shape[1] / size.height()

        img = cv2.resize(img, (size.width(), size.height()))
        # 如果是
        if len(img.shape) >= 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        x = img.shape[1]
        y = img.shape[0]
        if len(img.shape) >= 3:
            frame = QImage(img, x, y, x * 3, QImage.Format_RGB888)
        else:
            frame = QImage(img, x, y, x * 3, QImage.Format_Grayscale16)
        pix = QPixmap.fromImage(frame)
        item = QGraphicsPixmapItem(pix)  # 创建像素图元
        scene = graphicsView.scene()  # 创建场景
        scene.addItem(item)
        graphicsView.setScene(scene)
        graphicsView.show()
        return
