# 网格布局,计算机界面展示

import sys
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication


class GridLayoutExample(QWidget):
    def __init__(self):
        super(GridLayoutExample, self).__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']
        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            print(*position)  # 按钮坐标
            grid.addWidget(button, *position)
        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ge = GridLayoutExample()
    sys.exit(app.exec_())
