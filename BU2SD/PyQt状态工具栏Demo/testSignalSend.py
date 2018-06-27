# 判断信号是哪个组件发送的
import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMainWindow, QApplication


class Communicate(QObject):
    closeApp = pyqtSignal()  # 自定义一个信号


class SignalSend(QMainWindow):
    def __init__(self):
        super(SignalSend, self).__init__()
        self.initUI()

    def initUI(self):
        self.c = Communicate()
        self.c.closeApp.connect(self.close)  # 自定义信号连接着QMainWindow的close()槽

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mousePressEvent(self, event):
        self.c.closeApp.emit()  # 当在窗体上点击鼠标会触发closeApp信号,是程序退出


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ss = SignalSend()
    sys.exit(app.exec_())
