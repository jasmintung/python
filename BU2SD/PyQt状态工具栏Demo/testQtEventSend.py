# 事件发送者例子
import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication


class EventSendExample(QMainWindow):
    def __init__(self):
        super(EventSendExample, self).__init__()
        self.initUI()

    def initUI(self):
        btn1 = QPushButton('Button 1', self)
        btn1.move(50, 50)

        btn2 = QPushButton('Button 2', self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        # 创建一个状态
        # self.statusBar().showMessage('Ready')

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event sender')
        self.show()

    def buttonClicked(self):
        sender = self.sender()  # 通过sender()方法来判断信号源
        self.statusBar().showMessage(sender.text() + ' was pressed')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    se = EventSendExample()
    sys.exit(app.exec_())
