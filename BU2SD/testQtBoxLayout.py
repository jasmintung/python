# 盒布局

#  水平盒布局和垂直盒布局
'''
QHBoxLayout: 水平盒布局
QVBoxLayout: 垂直盒布局
'''
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication


class BoxLayoutExample(QWidget):
    def __init__(self):
        super(BoxLayoutExample, self).__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton("确定")
        cancelButton = QPushButton("取消")
        # 创建水平盒布局
        hbox = QHBoxLayout()
        # 让两个按钮始终在窗口右侧
        hbox.addStretch()  # 添加伸缩空间,函数的作用是在布局器中增加一个伸缩量，里面的参数表示QSpacerItem的个数，默认值为零，会将你放在layout中的空间压缩成默认的大小
        # 例如：一个layout布局器，里面有三个控件，一个放在最左边，一个放在最右边，最后一个放在layout的1/3处，这就可以通过addStretch去实现
        hbox.addWidget(okButton)
        # hbox.addStretch(10)  # 在两个按钮之间增加缩进
        hbox.addWidget(cancelButton)
        # 创建垂直布局,让水平布局显示在窗口底部
        vbox = QVBoxLayout()  # 我们创建一个水平布局和添加一个伸展因子和两个按钮。两个按钮前的伸展增加了一个可伸缩的空间。这将推动他们靠右显示
        vbox.addStretch()
        vbox.addLayout(hbox)  # 把水平布局加载到垂直布局中
        self.setLayout(vbox)  # 把垂直布局设置为窗口的主要布局
        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle("盒布局")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    be = BoxLayoutExample()
    sys.exit(app.exec_())


# 例子：用addStretch函数实现将nLayout的布局器的空白空间平均分配
#
# 在*.cpp中实现下列代码：
#
# //创建水平布局器
# QHBoxLayout *buttonLayout=new QHBoxLayout;
# button1=new QPushButton();
# button2=new QPushButton();
# button3=new QPushButton();
# buttonLayout->addStretch(1);  //增加伸缩量
# buttonLayout->addWidget(button1);
# buttonLayout->addStretch(1);  //增加伸缩量
# buttonLayout->addWidget(button2);
# buttonLayout->addStretch(1);  //增加伸缩量
# buttonLayout->addWidget(button3);
# buttonLayout->addStretch(6);  //增加伸缩量
# //void QWidget::setContentsMargins(int left, int top, int right, int bottom)
# //Sets the margins around the contents of the widget to have the sizes left, top, right, and bottom.
# //The margins are used by the layout system, and may be used by subclasses to specify the area to draw in (e.g. excluding the frame).
# buttonLayout->setContentsMargins(0,0,0,0);
# setLayout(buttonLayout);
#
# 程序运行后结果为：
#
# 其中四个addStretch()函数用于在button按钮间增加伸缩量，伸缩量的比例为1:1:1:6，意思就是将button以外的空白地方按设定的比例等分为9份并按照设定的顺序放入buttonLayout布局器中。