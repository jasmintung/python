# -*-coding:utf-8-*-
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog

from MainForm2 import Ui_MainWindow
from ChildrenForm2 import Ui_ChildrenForm


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)

        self.child = ChildrenForm()
        self.fileCloseAction.triggered.connect(self.close)
        self.fileOpenAction.triggered.connect(self.openMsg)
        self.addWinAction.triggered.connect(self.childShow)

    def childShow(self):
        # 添加子窗口
        self.MaingridLayout.addWidget(self.child)  # 在父窗口的Layout里面加上子窗口
        self.child.show()

    def openMsg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "ALL Files (*) ;;Text Files (*.txt)")
        print(file)  # 选中的文件名显示在状态栏
        self.statusbar.showMessage(file)


class ChildrenForm(QWidget, Ui_ChildrenForm):
    def __init__(self):
        super(ChildrenForm, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())
