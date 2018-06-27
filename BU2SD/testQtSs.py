# 信号槽例子,LCD的值会随着滑块的拖动而改变
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLCDNumber, QSlider, QVBoxLayout, QApplication


class SignalSlotsExample(QWidget):
    def __init__(self):
        super(SignalSlotsExample, self).__init__()
        self.initUI()

    def initUI(self):
        lcd = QLCDNumber(self)  # 创建LCD
        sld = QSlider(Qt.Horizontal, self)  # 创建滑块,滑块自身是水平摆放

        # 创建垂直盒布局
        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ss = SignalSlotsExample()
    sys.exit(app.exec_())
