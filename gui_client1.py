from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(463, 637)
        MainWindow.setStyleSheet("#err_cl , #dd_file{font-size:20px;}\n"
"#ip_server , #port_server{font-size:26px;}\n"
"#chon_file , #send{font-size: 30px;}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(170, 10, 151, 51))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 151, 41))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 150, 91, 41))
        self.label_3.setObjectName("label_3")
        self.ip_server = QtWidgets.QLineEdit(self.centralwidget)
        self.ip_server.setGeometry(QtCore.QRect(60, 110, 201, 31))
        self.ip_server.setText("")
        self.ip_server.setObjectName("ip_server")
        self.port_server = QtWidgets.QLineEdit(self.centralwidget)
        self.port_server.setGeometry(QtCore.QRect(60, 200, 201, 31))
        self.port_server.setText("")
        self.port_server.setObjectName("port_server")
        self.chon_file = QtWidgets.QPushButton(self.centralwidget)
        self.chon_file.setGeometry(QtCore.QRect(130, 440, 161, 61))
        self.chon_file.setObjectName("chon_file")
        self.send = QtWidgets.QPushButton(self.centralwidget)
        self.send.setGeometry(QtCore.QRect(130, 520, 161, 61))
        self.send.setObjectName("send")
        self.dd_file = QtWidgets.QLineEdit(self.centralwidget)
        self.dd_file.setGeometry(QtCore.QRect(110, 330, 341, 31))
        self.dd_file.setText("")
        self.dd_file.setObjectName("dd_file")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 327, 91, 41))
        self.label_4.setObjectName("label_4")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 463, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:26pt;\">CLIENT</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">IP ADDRESS:</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:14pt;\">PORT:</span></p></body></html>"))
        self.chon_file.setText(_translate("MainWindow", "Chọn file"))
        self.send.setText(_translate("MainWindow", "Gửi"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">File name:</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
