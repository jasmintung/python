# 整合状态、菜单、工具
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        # exitAction1 = QAction(QIcon('exit.png'), 'Exit', self)
        # exitAction1.setShortcut('Ctrl+Q')
        # exitAction1.setStatusTip('Exit application')
        # exitAction1.triggered.connect(self.close)

        self.statusBar().showMessage('Ready')
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        # toolbar.addAction(exitAction1)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
