# 绝对布局,程序制定每个组件的位置和大小(像素为单位)
# 绝对布局有以下限制:
#    如果我们调整窗口,组件的大小和位置不会改变
#    在各种平台上应用程序看起来可能会不一样
#    如果改变字体,我们的程序的布局就会改变
#    如果我们决定改变我们的布局,我们必须完全重做我们的布局
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication


class AbsoluteLayout(QWidget):
    def __init__(self):
        super(AbsoluteLayout, self).__init__()
        self.iniUI()

    def iniUI(self):
        label1 = QLabel("姓名", self)
        label1.move(10, 10)  # move方法控制组件的位置,相对主窗口边缘的位置
        label2 = QLabel("年龄", self)
        label2.move(35, 40)
        label3 = QLabel("所在城市", self)
        label3.move(55, 70)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle("绝对布局")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    al = AbsoluteLayout()
    sys.exit(app.exec_())
