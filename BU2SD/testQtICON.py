# 图标例子
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


class IConExample(QWidget):
    def __init__(self):
        super(IConExample, self).__init__()
        self.initUI()

    def initUI(self):
        # 同时设置窗口的位置、大小
        self.setGeometry(720, 480, 800, 600)
        # 设置窗口标题
        self.setWindowTitle("Icon")
        # 设置窗口图标,引用当前目录下的streamax.png图片
        self.setWindowIcon(QIcon('streamax.png'))
        # 显示窗口
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ie = IConExample()
    sys.exit(app.exec_())
