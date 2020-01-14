# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'filemanage.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QFileDialog


class Ui_Form(object):
    save_path = ''

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(484, 412)
        # self.save_path_but = QtWidgets.QPushButton(Form)
        # self.save_path_but.setGeometry(QtCore.QRect(380, 50, 75, 23))
        # self.save_path_text = QtWidgets.QLineEdit(Form)
        # self.save_path_text.setGeometry(QtCore.QRect(40, 50, 331, 20))
        # self.text_value = QtWidgets.QTextEdit(Form)
        # self.text_value.setGeometry(QtCore.QRect(10, 90, 461, 281))
        self.save_but = QtWidgets.QPushButton(Form)
        self.save_but.setGeometry(QtCore.QRect(190, 380, 75, 23))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        # self.save_path_but.setText(_translate("Form", "浏览"))
        # self.save_path_text.setPlaceholderText(_translate("Form", "保存地址"))
        self.save_but.setText(_translate("Form", "保存"))
        # self.save_path_but.clicked.connect(self.save_event)
        self.save_but.clicked.connect(self.save_text)

    # def save_event(self):
    #     global save_path
    #     _translate = QtCore.QCoreApplication.translate
    #     fileName2, ok2 = QFileDialog.getSaveFileName(None, "文件保存", "H:/")
    #     print(fileName2)  # 打印保存文件的全部路径（包括文件名和后缀名）
    #     save_path = fileName2
    #     self.save_path_text.setText(_translate("Form", save_path))

    def save_text(self):
        global save_path
        if save_path is not None:
            with open(file=save_path, mode='a+', encoding='utf-8') as file:
                file.write('hello world')
                # file.write(self.text_value.toPlainText())
            print('已保存！')
            # self.text_value.clear()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
