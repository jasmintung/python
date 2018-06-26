# 提示例子
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont


class NoticeExample(QWidget):
    def __init__(self):
        super(NoticeExample, self).__init__()
        self.initUI()

    def initUI(self):
        # 这种静态的方法设置一个用于显示工具提示的字体,我们使用10px
        QToolTip.setFont(QFont('SansSerif', 10))
        # 创建一个提示,我们称之为settooltip()方法.我们可以使用丰富的文本格式,鼠标移动到这个程序窗口的区域就显示
        self.setToolTip("This is a<b>Qwidget</b> widget")
        # 创建一个PushButton并为他设置一个tooltip,鼠标移动到按钮的区域就提示
        btn = QPushButton("Button", self)
        btn.setToolTip("This is a<b>QPushButton</b> widget")
        # 显示默认尺寸
        btn.resize(btn.sizeHint())
        # 移动按钮的位置
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ne = NoticeExample()
    sys.exit(app.exec_())
