# 窗口显示在屏幕中间
import sys
from PyQt5.QtWidgets import QWidget, QApplication


class ShowCenterExample(QWidget):
    def __init__(self):
        super(ShowCenterExample, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('Center')
        self.center()
        self.show()

    def center(self):
        desktop = app.desktop()
        print(desktop.width(), self.width())  # 注意这里有个现象如果是扩展了屏幕,这个值就不是一个屏幕的宽度了!
        print(desktop.height(), self.height())
        midWidth = (desktop.width() - self.width())/2
        midHeight = (desktop.height() - self.height())/2
        print(midWidth, midHeight)
        self.move(midWidth, midHeight)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ShowCenterExample()
    sys.exit(app.exec_())
