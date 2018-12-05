import sys
import threading
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPalette, QFont, QColor
from PyQt5.Qt import Qt, QCursor
from PyQt5.QtWidgets import QWidget, QLabel, QMessageBox, QAction, \
    QTextEdit, QHBoxLayout, QToolButton, QVBoxLayout, QGridLayout, \
    QMenu, QApplication


class BtnLabel(QLabel):
    """
    自定义一个类封装,处理QLabel点击事件
    """
    clicked = QtCore.pyqtSignal()
    moveOn = QtCore.pyqtSignal()
    moveLeave = QtCore.pyqtSignal()

    def __init__(self, lb_value):
        super(BtnLabel, self).__init__(lb_value)
        self.current_locate_label = None

    def mouseMoveEvent(self, e):
        self.setMouseTracking(True)
        self.moveOn.emit()

    def enterEvent(self, *args, **kwargs):
        # print(args)
        # print(kwargs)
        self.moveOn.emit()

    def leaveEvent(self, *args, **kwargs):
        self.moveLeave.emit()

    def mouseReleaseEvent(self, e):
        print("release:", e.button())
        if e.button() == Qt.LeftButton:  # 1表示鼠标左键,2表示鼠标右键
            self.clicked.emit()


class MisssionInterface(QWidget):
    end_app_signal = QtCore.pyqtSignal()
    font_locate_pe = QPalette()
    font_locate_pe.setColor(QPalette.WindowText, Qt.darkGreen)

    font_cancel_locate_pe = QPalette()
    font_cancel_locate_pe.setColor(QPalette.WindowText, Qt.darkGray)
    clicked_label_list = []  # 用来保存左边区域标签对象的列表

    def __init__(self, username, app):
        super(MisssionInterface, self).__init__()
        self.username = username
        self.app = app
        # 左边区域Label
        self.downloading = BtnLabel("正在下载")  # 正在下载
        self.downloading.setPalette(self.font_cancel_locate_pe)
        self.clicked_label_list.append(self.downloading)
        self.downloadfinished = BtnLabel("已完成")  # 下载已完成
        self.downloadfinished.setPalette(self.font_cancel_locate_pe)
        self.clicked_label_list.append(self.downloadfinished)
        self.uploading = BtnLabel("正在上传")  # 正在上传
        self.uploading.setPalette(self.font_cancel_locate_pe)
        self.clicked_label_list.append(self.uploading)
        self.uploadfinished = BtnLabel("已完成")  # 上传已完成
        self.uploadfinished.setPalette(self.font_cancel_locate_pe)
        self.clicked_label_list.append(self.uploadfinished)
        self.dustbin = BtnLabel("垃圾箱")  # 垃圾箱
        self.dustbin.setPalette(self.font_cancel_locate_pe)
        self.clicked_label_list.append(self.dustbin)
        # 右边区域按钮
        self.new_mission = QToolButton()  # 新建任务按钮
        self.start_mission = QToolButton()  # 开始任务按钮(开始所有任务)
        self.pause_mission = QToolButton()  # 暂停按钮
        self.delete_mission = QToolButton()  # 删除按钮
        self.close_window_btn = QToolButton()  # 关闭窗口
        self.minimum_window_btn = QToolButton()  # 最小化
        self.grid = QGridLayout()
        self.left_below_layout = QVBoxLayout()
        self.right_top_layout = QVBoxLayout()
        self.menu_button_layout = QHBoxLayout()  # 工具栏按钮水平布局
        self.title_line_layout = QHBoxLayout()
        # 一些状态的初始化
        self.is_locate_on_label = False
        self.initUI()

    def initUI(self):

        self.grid.setSpacing(10)  # 设置组件间间隔10个像素

        # 背景色
        pe = QPalette()
        pe.setColor(self.backgroundRole(), QColor(56, 73, 88))
        self.setPalette(pe)

        user_name = None
        if self.username is None:
            user_name = QLabel("humanbody")
        else:
            user_name = QLabel(self.username)
        user_name.setAlignment(Qt.AlignCenter)
        user_name.setFont(QFont('Fantasy', 20))  # 设置大小字体
        # 左下方布局

        self.left_below_layout.setSpacing(20)
        # left_below_layout.addStretch()  # 向下对齐

        self.downloading.setAlignment(Qt.AlignCenter)  # 居中显示
        self.downloading.setFont(QFont('Fantasy', 15))

        self.downloadfinished.setAlignment(Qt.AlignCenter)  # 居中显示
        self.downloadfinished.setFont(QFont('Fantasy', 15))

        self.uploading.setAlignment(Qt.AlignCenter)  # 居中显示
        self.uploading.setFont(QFont('Fantasy', 15))

        self.uploadfinished.setAlignment(Qt.AlignCenter)  # 居中显示
        self.uploadfinished.setFont(QFont('Fantasy', 15))

        self.dustbin.setAlignment(Qt.AlignCenter)  # 居中显示
        self.dustbin.setFont(QFont('Fantasy', 15))

        self.left_below_layout.addWidget(self.downloading)
        self.left_below_layout.addWidget(self.downloadfinished)
        self.left_below_layout.addWidget(self.uploading)
        self.left_below_layout.addWidget(self.uploadfinished)
        self.left_below_layout.addWidget(self.dustbin)
        self.left_below_layout.addStretch()  # 向上对齐
        self.downloading.clicked.connect(self.label_clicked)
        self.downloadfinished.clicked.connect(self.label_clicked)
        self.uploading.clicked.connect(self.label_clicked)
        self.uploadfinished.clicked.connect(self.label_clicked)
        self.dustbin.clicked.connect(self.label_clicked)

        self.downloading.moveOn.connect(self.label_locate)
        self.downloadfinished.moveOn.connect(self.label_locate)
        self.uploading.moveOn.connect(self.label_locate)
        self.uploadfinished.moveOn.connect(self.label_locate)
        self.dustbin.moveOn.connect(self.label_locate)

        self.downloading.moveLeave.connect(self.label_cancel_locate)
        self.downloadfinished.moveLeave.connect(self.label_cancel_locate)
        self.uploading.moveLeave.connect(self.label_cancel_locate)
        self.uploadfinished.moveLeave.connect(self.label_cancel_locate)
        self.dustbin.moveLeave.connect(self.label_cancel_locate)
        # 右上方布局
        self.title_line_layout.addStretch()  # 把关闭按钮抵到最右边
        self.close_window_btn.setIcon(QIcon('../../conf/icon/window_close.ico'))
        self.close_window_btn.clicked.connect(self.on_closewindow_btn_clicked)
        self.close_window_btn.setToolTip("<b>关闭</b>")
        self.minimum_window_btn.setIcon(QIcon('../../conf/icon/minum.ico'))
        self.minimum_window_btn.clicked.connect(self.on_miniumwindow_btn_clicked)
        self.minimum_window_btn.setToolTip("<b>最小化</b>")
        self.title_line_layout.addWidget(self.minimum_window_btn)
        self.title_line_layout.addWidget(self.close_window_btn)
        # menu_button_layout.addStretch()  # 增加缩进,在布局中添加空白，并把非空白内容顶到布局的尾部,右对齐

        # self.new_mission.setStyleSheet('QPushButton{border-image:url(../../conf/icon/pause.png)}')
        self.new_mission.setIcon(QIcon('../../conf/icon/new_mission.ico'))
        self.new_mission.setIconSize(QtCore.QSize(32, 32))  # 设置大小
        self.new_mission.setToolTip("<b>新建任务</b>")
        self.new_mission.setToolButtonStyle(Qt.ToolButtonIconOnly)  # 仅显示图片
        # self.new_mission.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.new_mission.setPopupMode(QToolButton.MenuButtonPopup)
        # self.new_mission.setAutoRaise(True)  # 3D帧
        pmenu = QMenu(self)
        self.puploadAct = QAction("上传任务", self)  # 按钮上加菜单选项
        self.pdownloadAct = QAction("下载任务", self)
        pmenu.addAction(self.puploadAct)
        pmenu.addAction(self.pdownloadAct)
        self.new_mission.setMenu(pmenu)

        self.start_mission.setIcon(QIcon('../../conf/icon/start.ico'))
        self.start_mission.setIconSize(QtCore.QSize(32, 32))  # 设置大小
        self.start_mission.setToolTip("<b>开始任务</b>")
        self.start_mission.clicked.connect(self.start_btn_clicked)

        self.pause_mission.setIcon(QIcon('../../conf/icon/pause.ico'))
        self.pause_mission.setIconSize(QtCore.QSize(32, 32))  # 设置大小
        self.pause_mission.setToolTip("<b>暂停</b>")
        self.pause_mission.clicked.connect(self.pause_btn_clicked)

        self.delete_mission.setIcon(QIcon('../../conf/icon/mission_delete.ico'))
        self.delete_mission.setIconSize(QtCore.QSize(32, 32))  # 设置大小
        self.delete_mission.setToolTip("<b>删除</b>")
        self.delete_mission.clicked.connect(self.delete_btn_clicked)

        self.menu_button_layout.addWidget(self.new_mission)
        self.menu_button_layout.addWidget(self.start_mission)
        self.menu_button_layout.addWidget(self.pause_mission)
        self.menu_button_layout.addWidget(self.delete_mission)
        self.menu_button_layout.addStretch()  # 在这里添加就是左对齐!!!!!
        self.right_top_layout.addLayout(self.title_line_layout)
        self.right_top_layout.addLayout(self.menu_button_layout)

        # 右下方布局
        text_area = QTextEdit()
        self.grid.addWidget(user_name, 1, 0)
        self.grid.addLayout(self.right_top_layout, 1, 1)
        self.grid.addLayout(self.left_below_layout, 2, 0)
        self.grid.addWidget(text_area, 2, 1)
        self.grid.setColumnStretch(0, 2)
        self.grid.setColumnStretch(1, 8)
        # 这句话将所有label组件应用
        # self.setStyleSheet(
        #      "QLabel{background:transparent; color:#cfe2f3; font-family:'Segoe UI'; font-size:15pt; border:none;}")
        self.resize(800, 600)
        self.setLayout(self.grid)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 无边框设置
        self.setWindowTitle("File Trans Tool")
        self.center()
        self.show()

        self.puploadAct.triggered.connect(self.new_menu_clicked)
        self.pdownloadAct.triggered.connect(self.new_menu_clicked)
        # print("init main window success")

    def center(self):
        desktop = self.app.desktop()
        midwidth = (desktop.width() - self.width())/2
        midheight = (desktop.height() - self.height())/2
        self.move(midwidth, midheight)

    def label_clicked(self):
        source = self.sender()
        print(source)
        if source in self.clicked_label_list:
            print("label clicked")
        # 哪个标签被点击了
        # if self.downloading == source:
        #     print("downloading")
        # elif self.dustbin == source:
        #     print("dustbin")

    def label_locate(self):
        """
        这个方法需要优化,再说吧
        :return:
        """
        self.is_locate_on_label = True
        source = self.sender()
        # print("locate:", source)
        self.current_locate_label = source
        if source in self.clicked_label_list:
            source.setPalette(self.font_locate_pe)

    def label_cancel_locate(self):
        source = self.sender()
        # print("cancel:", source)
        if self.current_locate_label == source:
            self.is_locate_on_label = False
            # print("reset color")
            self.current_locate_label.setPalette(self.font_cancel_locate_pe)

    # 以下通过重写窗口类再带的三个函数来实现窗口的拖动
    def mousePressEvent(self, event):
        """
        鼠标左键点击窗口任意位置
        :param event:
        :return:
        """
        if event.button() == Qt.LeftButton and not self.is_locate_on_label:  # 停留在最区域Label上时,不允许触发拖动事件
            self.drap_flag = True
            self.win_positon = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  # 更改鼠标的样子

    def mouseMoveEvent(self, event):
        """
        鼠标左键拖着窗口移动时
        :param event:
        :return:
        """
        if Qt.LeftButton and self.drap_flag:
            self.move(event.globalPos() - self.win_positon)  # 更改窗口位置
            event.accept()

    def mouseReleaseEvent(self, event):
        """
        鼠标左键松开
        :param event:
        :return:
        """
        self.drap_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

    def on_closewindow_btn_clicked(self):
        """
        关闭窗口
        :return:
        """
        self.close()

    def on_miniumwindow_btn_clicked(self):
        """
        最小化窗口
        :return:
        """
        self.showMinimized()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     '确定退出吗?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            # self.end_app_signal.emit()  # 发送关闭APP信号,未实现
            sys.exit(self.app.exec_())  # 这个方法简单粗暴
            # event.accept()  # 这个方法无法结束一些子线程
        else:
            event.ignore()

    def new_menu_clicked(self):
        print(self.sender())
        if self.sender() == self.pdownloadAct:
            print("down")
        elif self.sender() == self.puploadAct:
            print("upload")

    def start_btn_clicked(self):
        pass

    def pause_btn_clicked(self):
        pass

    def delete_btn_clicked(self):
        pass

    def add_upload_mission_dialog(self):
        """
        添加上传任务对话框
        :return:
        """


    def add_download_mission_dialog(self):
        """
        添加下载任务对话框
        :return:
        """


def initMissionUI(app):
    mi_win = MisssionInterface("张桐", app)
    sys.exit(app.exec_())

# 单独测试代码
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mi = MisssionInterface("张桐", app)
    sys.exit(app.exec_())
