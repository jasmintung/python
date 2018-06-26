import sys
from PyQt5.QtWidgets import QApplication, QWidget

# 每一个pyqt5程序必须创建一个应用程序对象,sys.argv参数是一个列表,从命令行输入参数.
app = QApplication(sys.argv)
# QWidget组件是pyqt5所有用户界面对象的基类,它为QWidget提供默认构造函数。默认构造函数没有基类
w = QWidget()
# 设置窗口大小单位px
w.resize(250, 150)
# 移动窗口在屏幕上的位置到x = 300, y = 300坐标
w.move(300, 300)
# 设置窗口的标题
w.setWindowTitle("BU2SD Tool")
# 显示在屏幕上
w.show()
# 系统exit()方法确保应用程序干净的退出,exec_()方法
sys.exit(app.exec_())
