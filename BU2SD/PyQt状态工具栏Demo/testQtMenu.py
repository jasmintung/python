# 菜单栏例子
import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon


class MenuExample(QMainWindow):
    def __init__(self):
        super(MenuExample, self).__init__()
        self.initUI()

    def initUI(self):
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)  # 菜单项的图片后跟标签文字Exit
        exitAction.setShortcut('Ctrl+Q')  # 设置快捷键,退出,并在菜单项上也会显示出来,真好
        exitAction.setStatusTip('Exit Application')  # 鼠标移到菜单项时提示
        exitAction.triggered.connect(qApp.quit)  # 终止应用程序

        # 创建一个状态栏
        self.statusBar().showMessage('Ready')
        # 创建一个菜单栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')  # 添加菜单,命名叫File
        fileMenu.addAction(exitAction)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    me = MenuExample()
    sys.exit(app.exec_())
