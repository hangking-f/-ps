import sys
from PyQt5.Qt import *
from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from PyQt5.QtWidgets import QComboBox

import cv2
import picture_chuli



class My_PS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('图像处理')
        self.resize(1500, 900)

        wid = 1400
        hgt = 720

        #按钮背景
        self.back = QLabel(self)
        self.back.setFixedSize(1500, 0.1 * 900)
        self.back.setStyleSheet("QLabel{background:red;}")

        #图片区
        self.label_pic = QLabel(self)
        self.label_pic.setFixedSize(wid,hgt)
        self.label_pic.move(50, 100)
        self.label_pic.setFrameShape(QtWidgets.QFrame.Box)
        self.label_pic.setLineWidth(1)
        self.label_pic.setStyleSheet("QLabel{background:pink;}")

        #原图展示区
        self.label_daichuli = QtWidgets.QLabel(self.label_pic)
        self.label_daichuli.setGeometry(QtCore.QRect(wid/2-500,100,400,500))
        self.label_daichuli.setObjectName("label_daichuli")
        self.label_daichuli.setFrameShape(QtWidgets.QFrame.Box)
        self.label_daichuli.setLineWidth(1)
        self.label_daichuli.setStyleSheet("QLabel{background:white;}")

        #效果展示区
        self.label_result = QtWidgets.QLabel(self.label_pic)
        self.label_result.setGeometry(QtCore.QRect(wid/2+100, 100, 400, 500))
        self.label_result.setObjectName("label_daichuli")
        self.label_result.setFrameShape(QtWidgets.QFrame.Box)
        self.label_result.setLineWidth(1)
        self.label_result.setStyleSheet("QLabel{background:white;}")


        #按钮全局布局

        hlayout1 = QtWidgets.QVBoxLayout()
        hlayout1.setContentsMargins(50,10,1100,10)


        #打开图片按钮
        self.pushbutton_openimg = QtWidgets.QPushButton()
        self.pushbutton_openimg.setText("打开图片")
        self.pushbutton_openimg.clicked.connect(self.openimage)

        #保存图片按钮
        self.pushbtton_save = QtWidgets.QPushButton()
        self.pushbtton_save.setText("保存图片")
        self.pushbtton_save.clicked.connect(self.saveimage)

        #旋转按钮
        a = 500
        self.zuoxuan = QtWidgets.QPushButton(self.back)
        self.zuoxuan.setText("顺时针旋转")
        self.zuoxuan.clicked.connect(self.shunshizhen)
        self.zuoxuan.move(a,10)
        self.youxuan = QtWidgets.QPushButton(self.back)
        self.youxuan.setText("逆时针旋转")
        self.youxuan.clicked.connect(self.nishizhen)
        self.youxuan.move(a+100,10)
        self.jingxiang = QtWidgets.QPushButton(self.back)
        self.jingxiang.setText("镜像")
        self.jingxiang.clicked.connect(self.jingxiang1)
        self.jingxiang.move(a,50)
        self.shangxia = QtWidgets.QPushButton(self.back)
        self.shangxia.setText("上下颠倒")
        self.shangxia.clicked.connect(self.shangxia1)
        self.shangxia.move(a+100,50)

        # 加噪按钮
        self.lineEdit_n_value = QtWidgets.QLineEdit(self.back)
        self.lineEdit_n_value.setFixedSize(130,30)
        self.lineEdit_n_value.move(a+300,10)
        self.lineEdit_n_value.setText("1000")
        self.addnoise = QtWidgets.QPushButton(self.back)
        self.addnoise.move(a+450,10)
        self.addnoise.setText("添加椒盐噪音")
        self.addnoise.clicked.connect(self.addnoise1)
        self.lineEdit_mean_value = QtWidgets.QLineEdit(self.back)
        self.lineEdit_mean_value.move(a+300, 50)
        self.lineEdit_mean_value.setText("0")
        self.lineEdit_mean_value.setFixedSize(60,30)
        self.lineEdit_sigma_value = QtWidgets.QLineEdit(self.back)
        self.lineEdit_sigma_value.setText("25")
        self.lineEdit_sigma_value.move(a + 365, 50)
        self.lineEdit_sigma_value.setFixedSize(60, 30)
        self.addnoisy = QtWidgets.QPushButton(self.back)
        self.addnoisy.move(a+450,50)
        self.addnoisy.setText("添加高斯噪音")
        self.addnoisy.clicked.connect(self.addnoisy1)



        hlayout1.addWidget(self.pushbutton_openimg)
        hlayout1.addWidget(self.pushbtton_save)
        self.back.setLayout(hlayout1)


        # 实例化QComBox对象
        self.cb = QComboBox(self.back)

        self.cb.move(1150, 25)
        items = ["灰度", "二值化", "拉普拉斯","伽马变化","轮廓","sift检测","浮雕效果","水彩效果",
                 "中值滤波","高斯滤波","均值滤波","图像修复"]
        self.cb.addItems(items)

        # # 信号
        self.cb.currentIndexChanged[int].connect(self.print_value) # 条目发生改变，发射信号，传递条目内容
        # self.cb.highlighted[str].connect(self.print_value)  # 在下拉列表中，鼠标移动到某个条目时发出信号，传递条目内容

    def openimage(self):  # 选择本地图片上传
        # 弹出一个文件选择框，第一个返回值imgName记录选中的文件路径+文件名，第二个返回值imgType记录文件的类型
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "","*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(imgName).scaled(self.label_daichuli.width(),
                                            self.label_daichuli.height())  # 通过文件路径获取图片文件，并设置图片长宽为label控件大小j
        self.label_daichuli.setPixmap(jpg)  # 在label控件上显示选择的图片

    def saveimage(self):  # 保存图片到本地
        screen = QApplication.primaryScreen()
        pix = screen.grabWindow(self.label_result.winId())
        fd, type = QFileDialog.getSaveFileName(self, "保存图片", "", "*.jpg;;*.png;;All Files(*)")
        pix.save(fd)

    # a=["huidutu","erzhihua"]

    def print_value(self, i):
        self.caozuo(i)

    def caozuo(self,i):
        qimg = self.label_daichuli.pixmap()
        src = qtpixmap_to_opencv(qimg)
        if i == 0: ##亦可用switch方法
            newsrc = picture_chuli.gray_picture(src)
        elif i == 1:
            newsrc = picture_chuli.erzhihua(src)
        elif i == 2:
            newsrc = picture_chuli.laplas(src)
        elif i == 3:
            newsrc = picture_chuli.gama(src)
        elif i == 4:
            newsrc = picture_chuli.morphologyExfun(src)
        elif i == 5:
            newsrc = picture_chuli.sift_fun(src)
        elif i == 6:
            newsrc = picture_chuli.fudiao_fun(src)
        elif i == 7:
            newsrc = picture_chuli.shuicai_fun(src)
        elif i == 8:
            newsrc = picture_chuli.medianBlurfun(src)
        elif i == 9:
            newsrc = picture_chuli.GaussianBlurfun(src)
        elif i == 10:
            newsrc = picture_chuli.blurfun(src)
        elif i == 11:
            newsrc = picture_chuli.xiufu(src)

        pix = opencv_to_qtpixmap(newsrc)
        self.label_result.setPixmap(pix)


    def addnoise1(self):
        qimg = self.label_daichuli.pixmap()
        src = qtpixmap_to_opencv(qimg)
        num = self.lineEdit_n_value.text()
        num = int(num)
        newsrc = picture_chuli.jynoisy(src, num)
        pix = opencv_to_qtpixmap(newsrc)
        self.label_result.setPixmap(pix)

    def addnoisy1(self):
        qimg = self.label_daichuli.pixmap()
        src = qtpixmap_to_opencv(qimg)
        mean = self.lineEdit_mean_value.text()
        mean = int(mean)
        sigma = self.lineEdit_sigma_value.text()
        sigma = int(sigma)
        newsrc = picture_chuli.gsnoise(src, mean, sigma)
        pix = opencv_to_qtpixmap(newsrc)
        self.label_result.setPixmap(pix)

    def shangxia1(self):
        qimg = self.label_daichuli.pixmap()
        src = qtpixmap_to_opencv(qimg)
        newsrc = picture_chuli.sxfun(src)
        pix = opencv_to_qtpixmap(newsrc)
        self.label_result.setPixmap(pix)

    def jingxiang1(self):
        qimg = self.label_daichuli.pixmap()
        src = qtpixmap_to_opencv(qimg)
        newsrc = picture_chuli.flipfun(src)
        pix = opencv_to_qtpixmap(newsrc)
        self.label_result.setPixmap(pix)

    def shunshizhen(self):
        qimg = self.label_daichuli.pixmap()
        src = qtpixmap_to_opencv(qimg)
        newsrc = picture_chuli.RotateClockWise90(src)
        pix = opencv_to_qtpixmap(newsrc)
        self.label_result.setPixmap(pix)


    def nishizhen(self):
        qimg = self.label_daichuli.pixmap()
        src = qtpixmap_to_opencv(qimg)
        newsrc = picture_chuli.RotateAntiClockWise90(src)
        pix = opencv_to_qtpixmap(newsrc)
        self.label_result.setPixmap(pix)




def qtpixmap_to_opencv(qtpixmap):    #qtpixmap转opencv
    qimg = qtpixmap.toImage()
    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]
    return result


def opencv_to_qtpixmap(cvimg):
    if cvimg.ndim==2:              #单通道
        height, width= cvimg.shape
        cvimg = cv2.cvtColor(cvimg, cv2.COLOR_BGR2RGB)
        cvimg = QImage(cvimg.data, width, height, QImage.Format_RGB888)
        pix = QPixmap.fromImage(cvimg)
        return pix
    else:                          #多个通道
        width = cvimg.shape[1]
        height = cvimg.shape[0]
        pixmap = QPixmap(width, height)  # 根据已知的高度和宽度新建一个空的QPixmap,
        qimg = pixmap.toImage()         # 将pximap转换为QImage类型的qimg
        for row in range(0, height):
            for col in range(0, width):
                b = cvimg[row, col, 0]
                g = cvimg[row, col, 1]
                r = cvimg[row, col, 2]
                pix = qRgb(r, g, b)
                qimg.setPixel(col, row, pix)
                pix = QPixmap.fromImage(qimg)
        return pix



if __name__ == '__main__':
    app = QApplication(sys.argv)
    Ps = My_PS()
    Ps.show()
    sys.exit(app.exec_())
