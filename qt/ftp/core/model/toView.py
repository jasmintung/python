from PyQt5 import QtCore
from core.control import testsend
import time


class Runthread(QtCore.QObject):
    update_text_signal = QtCore.pyqtSignal(str)  # 创建一个信号

    def __init__(self, type, parent=None):
        super(Runthread, self).__init__(parent)
        self.type = type

    def run(self):
        """
        这里进行
        :return:
        """
        if self.type == 0:
            testsend.start_login_check(self.callback)
        else:
            pass

    def callback(self, msg):
        """
        通过control层封装回调进行信号换发
        :param msg:
        :return:
        """
        self.update_text_signal.emit(msg)
