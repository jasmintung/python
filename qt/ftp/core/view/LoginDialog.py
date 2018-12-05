# 登陆界面
import sys
from core.view import MissionUI
from conf import settings
from core.model.toView import Runthread
from PyQt5 import QtCore, QtGui
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, QGridLayout, QVBoxLayout, QHBoxLayout, QApplication


class FTPClientLoginDialog(QDialog):
    login_result_signal = QtCore.pyqtSignal(str)

    def __init__(self, app):
        super(FTPClientLoginDialog, self).__init__()
        self.name = ""
        self.password = ""
        self.ip = ""
        self.app = app
        self.init_ui()

    def init_ui(self):
        self.resize(settings.LOGIN_PAGE_SIZE["width"], settings.LOGIN_PAGE_SIZE["height"])
        self.setWindowTitle(settings.LOGIN_TITLE)
        self.center_coordinate_get()

        username = QLabel("用户名", self)
        password = QLabel("密码", self)
        ip = QLabel("登陆Ip", self)
        login_button = QPushButton("登陆")
        login_button.setSizePolicy(20, 20)
        # login_button.move(20, 100)

        self.name_edit = QLineEdit()  # 用户名输入框
        self.pwd_edit = QLineEdit()  # 密码输入框
        self.ip_edit = QLineEdit()  # IP地址输入框

        self.pwd_edit.setEchoMode(QLineEdit.Password)  # 密码隐蔽输入

        # 登陆进程显示
        self.statue = QLabel()
        self.statue.move(120, 20)
        # self.statue.setDisabled(True)

        grid = QGridLayout()  # 网格布局
        grid.setSpacing(10)  # 设置组件间的间隔,10个像素
        grid.addWidget(username, 1, 0)
        grid.addWidget(self.name_edit, 1, 1)
        grid.addWidget(password, 2, 0)
        grid.addWidget(self.pwd_edit, 2, 1)
        grid.addWidget(ip, 3, 0)
        grid.addWidget(self.ip_edit, 3, 1)

        below = QHBoxLayout()  # 水平布局
        below.addWidget(login_button)
        below.addWidget(self.statue)
        layout = QVBoxLayout()  # 垂直布局
        layout.addLayout(grid)
        layout.addLayout(below)
        # 各组件添加信号绑定槽
        self.name_edit.textChanged[str].connect(self.on_line_edit_changed)
        self.pwd_edit.textChanged[str].connect(self.on_line_edit_changed)
        self.ip_edit.textChanged[str].connect(self.on_line_edit_changed)
        login_button.clicked.connect(self.on_button_clicked)
        # 设置总体布局
        self.setLayout(layout)
        self.show()

    def center_coordinate_get(self):
        """
        获取屏幕中心位置坐标,注意如果是双屏的话,本方法不适用,因为双屏的宽度是两个屏幕的和,但怎么判断是不是双屏呢?
        :return:
        """
        desktop = self.app.desktop()
        mid_width = (desktop.width() - self.width())/2
        mid_height = (desktop.height() - self.height())/2
        self.move(mid_width, mid_height)

    def on_line_edit_changed(self, text):
        """
        得到编辑框编辑信息
        :param text: 编辑框输入的数据
        :return:
        """
        source = self.sender()
        if source == self.name_edit:
            self.name = text
        elif source == self.pwd_edit:
            self.password = text
        elif source == self.ip_edit:
            self.ip = text

    def on_button_clicked(self):
        """
        得到按钮按下的情况
        :return:
        """
        source = self.sender()
        if source.text() == '登陆':
            self.statue.setDisabled(False)
            self.statue.setText("登陆...")
            # 创建线程
            self.obj = Runthread(0)
            # 连接信号
            self.obj.update_text_signal.connect(self.login_process)
            # 开始线程
            self.mythread = QtCore.QThread()
            self.obj.moveToThread(self.mythread)
            self.mythread.started.connect(self.obj.run)
            self.mythread.start()

    def login_process(self, text):
        self.statue.setText(text)
        if text == "登陆完成":
            # MissionUI.initMissionUI()
            # self.close()
            # print()
            # self.mythread.quit()
            # self.login_result_signal.emit("OK")
            self.close()
            self.accept()  # 这里是界面跳转的关键!!!!!!
        else:
            self.login_result_signal.emit("not pass")
            # MissionUI.initMissionUI()
            # self.close()
            # QtCore.QCoreApplication.quit()


def init(app):
    fld = FTPClientLoginDialog(app)
    return fld
    # sys.exit(app.exec_())
