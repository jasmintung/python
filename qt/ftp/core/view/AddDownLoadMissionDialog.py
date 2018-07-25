import sys
from PyQt5 import Qt
from PyQt5.QtWidgets import QDialog, QLabel, QTextEdit, QPushButton, QVBoxLayout, QApplication


class AddDLMD(QDialog):
    def __init__(self):
        super(AddDLMD, self).__init__()
        self.initDg()

    def initDg(self):
        self.setWindowTitle("新建下载任务")
        layout = QVBoxLayout()
        downloadLinklb = QLabel("下载链接: ")
        linksArea = QTextEdit()
        linksArea.setPlaceholderText("(多个URL请回车换行)")  # 设置默认提示,有输入自动清空
        dnbg = QPushButton("立即下载")
        dnbg.setSizePolicy(20, 20)
        dnbg.clicked.connect(self.beginDownLoadTasks)

        layout.addWidget(downloadLinklb)
        layout.addWidget(linksArea)
        layout.addWidget(dnbg)
        layout.addStretch()
        self.resize(500, 200)
        self.setLayout(layout)
        self.show()

    def beginDownLoadTasks(self):
        pass


# 独立单元测试代码
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ad = AddDLMD()
    sys.exit(app.exec_())
