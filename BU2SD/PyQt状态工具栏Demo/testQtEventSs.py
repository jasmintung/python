# 重写事件处理方法例子
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication


class RewriteEventSignalSlotsExample(QWidget):
    def __init__(self):
        super(RewriteEventSignalSlotsExample, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(30, 360, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()

    def keyPressEvent(self, e):
        # 重写keyPressEvent事件处理器,按下Esc会退出程序
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    rs = RewriteEventSignalSlotsExample()
    sys.exit(app.exec_())
