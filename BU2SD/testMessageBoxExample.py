# 提示框
import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication


class MessageBoxExample(QWidget):
    def __init__(self):
        super(MessageBoxExample, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Message box')
        self.show()

    def closeEvent(self, event):
        # 重写closeEvent方法,第二个参数出现在titlebar.第三个参数是对话框中显示的文本,
        # 第四个参数指定按钮的组合出现在对话框中.最后一个参数是默认按钮,这个是默认的按钮焦点.
        # 这个对话框的显示默认在程序主窗口的中间位置
        reply = QMessageBox.question(self, 'Message',
                                     'Are u sure to quit?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mbex = MessageBoxExample()
    sys.exit(app.exec_())
