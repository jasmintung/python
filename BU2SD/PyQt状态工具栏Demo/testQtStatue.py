# 状态显示例子
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class StatueShow(QMainWindow):
    def __init__(self):
        super(StatueShow, self).__init__()
        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Ready')  # 创建一个状态栏,状态栏显示的消息是"Ready"
        self.setGeometry(300, 300, 250, 150)  # 状态消息默认显示在窗口的左下角
        self.setWindowTitle('Statusbar')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ss = StatueShow()
    sys.exit(app.exec_())
