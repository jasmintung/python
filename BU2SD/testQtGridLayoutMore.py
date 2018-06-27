# 网格布局例子, 评论
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication


class GridLayoutMoreExample(QWidget):
    def __init__(self):
        super(GridLayoutMoreExample, self).__init__()
        self.initUI()

    def initUI(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()  # 行编辑
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()  # 文本编辑

        grid = QGridLayout()
        grid.setSpacing(10)  # 设置组件间的间隔,10个像素

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)  # 这个地方还有疑问,什么叫跨度

        self.setLayout(grid)
        self.setWindowTitle("Review")
        self.setGeometry(300, 300, 350, 300)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gme = GridLayoutMoreExample()
    sys.exit(app.exec_())
