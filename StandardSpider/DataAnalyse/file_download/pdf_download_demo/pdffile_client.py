import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMessageBox
from file_spider import pdffile_to_fdfs


class MyWindow(QtWidgets.QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.resize(500, 100)
        self.setWindowTitle("Mouser爬虫 - 附件")
        self.worker = MyWorker()
        _translate = QtCore.QCoreApplication.translate

        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.label.setText(_translate("Dialog", "<span style=\" font-weight:600;\">请输入账号</span>"))
        self.label.setFixedWidth(80)
        # 用户名输入框
        self.nameEdit = QtWidgets.QLineEdit(self)
        self.nameEdit.setObjectName("nameEdit")

        self.threadLabel = QtWidgets.QLabel(self)
        self.threadLabel.setObjectName("threadLabel")
        self.threadLabel.setText(_translate("Dialog", "<span style=\" font-weight:600;\">线程数</span>"))
        self.threadLabel.setFixedWidth(50)
        # 线程输入框
        self.threadEdit = QtWidgets.QLineEdit(self)
        self.threadEdit.setObjectName("threadEdit")
        self.threadEdit.setFixedWidth(50)
        self.threadEdit.setText('10')
        # 开始按钮
        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setObjectName("startButton")
        self.startButton.setText("开始")
        self.startButton.setFixedWidth(70)
        self.startButton.clicked.connect(self.start)
        # 取消按钮
        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("取消")
        self.cancelButton.setFixedWidth(70)
        self.cancelButton.clicked.connect(self.close)
        # 状态统计
        self.statLabel = QtWidgets.QLabel(self)
        self.statLabel.setObjectName("statLabel")
        # 布局
        self.grid = QtWidgets.QGridLayout(self)
        self.grid.addWidget(self.label, 1, 0)
        self.grid.addWidget(self.nameEdit, 1, 1)
        self.grid.addWidget(self.threadLabel, 1, 2)
        self.grid.addWidget(self.threadEdit, 1, 3)
        self.grid.addWidget(self.startButton, 1, 4)
        self.grid.addWidget(self.cancelButton, 1, 5)
        self.grid.addWidget(self.statLabel, 2, 0, 1, 6)

        # 信号
        self.worker.stat_signal.connect(self._update_stat)

    def _update_stat(self, succeed, failured, active, total):
        self.statLabel.setText("成功 %s,失败 %s,正在爬取 %s" % (succeed, failured, active))

    def start(self):
        name = self.nameEdit.text()
        thread = self.threadEdit.text()
        if len(name) == 0:
            QMessageBox.information(self, "提示", "请先输入您的账号，输入不存在的账号会自动创建")
        elif len(thread) == 0:
            QMessageBox.information(self, "提示", "请先输入您开启的线程数，比如10")
        else:
            self.nameEdit.setDisabled(True)
            self.threadEdit.setDisabled(True)
            self.startButton.setDisabled(True)
            self.worker.setName(name)
            self.worker.setThreadSize(int(thread))
            try:
                self.worker.start()
            except:
                None


class MyWorker(QtCore.QThread):
    stat_signal = QtCore.pyqtSignal(int, int, int, int)

    def __init__(self, userName=None, threadSize=10):
        super(MyWorker, self).__init__()
        self.userName = userName
        self.threadSize = threadSize

    def setName(self, userName):
        self.userName = userName

    def setThreadSize(self, threadSize):
        self.threadSize = threadSize

    def run(self):
        spider = pdffile_to_fdfs.FileMain(userName=self.userName, maxThread=self.threadSize)
        while spider.hasNext():
            spider.craw()
            self.stat_signal.emit(*spider.statistic())


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())
