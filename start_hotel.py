import csv
import ctypes
import inspect
import sys
import threading
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from OperateData import OperateSql
from window import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.setWindowTitle('携程酒店')

    def init_ui(self):
        self.op = OperateSql()
        self.show_all()
        # self.op.show_num.connect(self.show_num)
        # self.op.show_data.connect(self.show_d)
        self.pushButton_3.clicked.connect(self.set_data)
        self.pushButton.clicked.connect(self.save_file)
        # self.pushButton_2.clicked.connect(self.quit_sys)

    def show_all(self):
        self.thread = threading.Thread(target=self.op.start_task)
        self.thread.start()
        self.op.show_num.connect(self.show_num)
        self.op.show_data.connect(self.show_d)

    def set_data(self):
        print("set_data")
        self.progressBar.setValue(0)
        print('222')
        self.thread = threading.Thread(target=self.op.read_excel)
        self.thread.start()
        self.op.show_bar.connect(self.show_bar)

    def show_bar(self, value):
        self.progressBar.setValue(value)

    def show_num(self, value):
        print('show_num')
        # print(value)
        max_num = value[0]
        hotel_num = value[1]
        self.lineEdit_3.setText(str(max_num))
        self.lineEdit_4.setText(str(hotel_num))

    def show_d(self, value):
        print("show_d")
        self.textEdit.clear()
        # print(value)
        con = '\n'.join(value)
        self.textEdit.setText(con)

    def save_file(self):
        print("save_file")
        data_str = self.textEdit.toPlainText()
        data_list = data_str.split('\n')
        if os.path.exists(r'已抓酒店数据.csv'):
            os.remove(r'已抓酒店数据.csv')
        for data in data_list:
            with open(r'已抓酒店数据.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, dialect='excel')
                writer.writerow([data])
        print('酒店保存成功!!!')
        self.showMessage()
        # self.thread = threading.Thread(target=self.xc.start_task, args=(data,))
        # self.thread.start()

    def quit_sys(self):
        self.xc.quit_driver()
        try:
            if self.thread.isAlive():
                self._asybc_raise(self.thread.ident, SystemExit)
        except:
            pass
        sys.exit()

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())
