import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from MainForm import Ui_MainWindow


class MainForm(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        # 事件连接槽方法close
        self.fileCloseAction.triggered.connect(self.close)
        # 事件连接槽方法openMsg
        self.fileOpenAction.triggered.connect(self.openMsg)

    def openMsg(self):
        file, ok = QFileDialog.getOpenFileName(self, "打开", "C:/", "ALL Files (*) ;;Text Files (*.txt)")
        print(file)  # 选中的文件名显示在状态栏
        self.statusbar.showMessage(file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainForm()
    win.show()
    sys.exit(app.exec_())
