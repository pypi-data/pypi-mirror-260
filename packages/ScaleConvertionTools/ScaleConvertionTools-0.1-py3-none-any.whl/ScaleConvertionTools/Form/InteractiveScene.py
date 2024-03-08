# -*- coding: utf-8 -*-
# @Time    : 2024/3/5 16:05
# @Author  : qxcnwu
# @FileName: InteractiveScene.py
# @Software: PyCharm
from functools import partial

import cv2
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPen, QBrush, QFont, QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent, QTableWidget, QGraphicsPixmapItem, QGraphicsView, \
    QPushButton
from qtpy import QtWidgets

from ScaleConvertionTools.CommonObject.TmpFile import Tmp
from ScaleConvertionTools.DataProcess.SedProcess import decode_sed


class InteractiveScene(QGraphicsScene):
    def __init__(self, qList: QTableWidget, gf: QGraphicsView):
        super().__init__()
        self.startx = None
        self.starty = None
        self.temp_rect = []
        self.rect = []
        self.text = []
        self.scale = 1
        self.line = []
        self.font = QFont()
        self.font.setPixelSize(24)
        self._bro = None
        self._qList = qList
        self.sed = {}
        self.gf = gf

    def add_bro(self, bro):
        """
        添加兄弟对象
        :return:
        """
        self._bro = bro
        return

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        """
        当前的点击事件
        :param event:
        :return:
        """
        if event.button() == Qt.LeftButton:
            self.startx = event.scenePos().x()
            self.starty = event.scenePos().y()
        return

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        """
        鼠标施放事件
        :param event:
        :return:
        """

        if event.button() == Qt.LeftButton:
            if self.startx is None and self.starty is None:
                return
            self.removeLine()
            # 添加
            x1, y1, x2, y2 = self.get_points(event.scenePos())
            # 判断合法性
            if x2 >= self.width() or x1 < 0 or y2 > self.height() or y1 < 0:
                return
            self.temp_rect.append([x1, y1, x2, y2])
            rect = self.addRect(x1, y1, x2 - x1, y2 - y1, QPen(Qt.black), QBrush(Qt.white))

            text_item = self.addText(str(len(self.temp_rect)))
            text_item.setFont(self.font)
            text_item.setPos(x1 + 12, y1 + 12)

            self.text.append(text_item)
            self.addItem(rect)
            self.rect.append(rect)
            self.startx = None
            self.starty = None

            # 判断
            self.query_add_list()

        elif event.button() == Qt.RightButton:
            # 删除
            if len(self.temp_rect) == 0:
                return
            self.removeItem(self.text[-1])
            self.text = self.text[:-1]
            self.removeItem(self.rect[-1])
            self.temp_rect = self.temp_rect[:-1]
            self.rect = self.rect[:-1]
            self.startx = None
            self.starty = None

            # 判断
            self.query_add_list()

        return

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        """
        移动鼠标
        :param event:
        :return:
        """
        if self.startx is None or self.starty is None:
            return
        pos = event.scenePos()
        x1, y1, x2, y2 = self.get_points(pos)
        # 超出范围
        if x2 >= self.width() or x1 < 0 or y2 > self.height() or y1 < 0:
            return
        # 移动
        self.removeLine()
        self.line.append(self.addLine(x1, y1, x1, y2, QPen(Qt.black)))
        self.line.append(self.addLine(x1, y2, x2, y2, QPen(Qt.black)))
        self.line.append(self.addLine(x2, y2, x2, y1, QPen(Qt.black)))
        self.line.append(self.addLine(x2, y1, x1, y1, QPen(Qt.black)))
        return

    def get_points(self, point: QPointF):
        """
        获取坐标点
        :return:
        """
        endx = point.x()
        endy = point.y()
        x1 = min(endx, self.startx)
        x2 = max(endx, self.startx)
        y1 = min(endy, self.starty)
        y2 = max(endy, self.starty)
        return x1, y1, x2, y2

    def removeLine(self):
        # 删除直线
        for item in self.line:
            self.removeItem(item)
        self.line = []
        return

    def query_add_list(self):
        """
        添加选择对象
        :return:
        """
        size = min(len(self.rect), len(self._bro.rect))
        # 判断当前是添加还是删除
        row = self._qList.rowCount()
        if row <= size:
            self._qList.setRowCount(size)
            for i in range(row, size):
                self._qList.setCellWidget(i, 0, self.buttonForRow(i))
        else:
            self._qList.setRowCount(size)
        return

    def buttonForRow(self, idx: int):
        """
        添加按钮
        :return:
        """
        widget = QtWidgets.QWidget()
        # 修改
        updateBtn = QtWidgets.QPushButton('导入地表反射率')
        updateBtn.setStyleSheet(''' text-align : center;
                                             background-color : NavajoWhite;
                                             height : 30px;
                                             font : 13px  ''')
        updateBtn.clicked.connect(partial(self.add_event_slot, idx, updateBtn))
        hLayout = QtWidgets.QHBoxLayout()
        hLayout.addWidget(updateBtn)
        hLayout.setContentsMargins(5, 2, 5, 2)
        widget.setLayout(hLayout)
        return widget

    def add_event_slot(self, idx: int, updateBtn: QPushButton):
        sed_path = QtWidgets.QFileDialog.getOpenFileName(None, "选取数据文件", "./",
                                                         "Data Files (*.xls *.csv *.xlsx);;All Files (*)")[0]
        if sed_path is None:
            return
        updateBtn.setText(sed_path)
        self.sed[idx] = sed_path
        self.plot()
        return

    def plot(self):
        for it in self.sed.keys():
            wave, ref = decode_sed(self.sed[it])
            plt.plot(wave, ref, label=str(it))
        plt.xlabel("wave length(nm)")
        plt.ylabel("ref")
        plt.ylim(0, 1)
        plt.legend()
        plt.subplots_adjust()
        plt.savefig(Tmp.plot_ref_path_name)
        plt.close()
        self.qt_load_image()
        return

    def qt_load_image(self):
        """
        导入图像
        :param image_path:
        :param graphicsView:
        :return:
        """
        size = self.gf.geometry()
        img = cv2.imread(Tmp.plot_ref_path_name)
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
        scene = QGraphicsScene()  # 创建场景
        scene.addItem(item)
        self.gf.setScene(scene)
        self.gf.show()
        return
