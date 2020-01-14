import csv
import ctypes
import inspect
import sys
import threading
import os
from PyQt5.QtWidgets import QMainWindow, QApplication
from hotel_list import HotelList
from hotelwindow import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.setWindowTitle('携程酒店搜索')

    def init_ui(self):
        self.pushButton_2.clicked.connect(self.show_all)
        self.pushButton.clicked.connect(self.save_file)
        self.pushButton_3.clicked.connect(self.quit_sys)

    def show_all(self):
        self.hl = HotelList()
        self.keysword = self.lineEdit.text()
        self.thread = threading.Thread(target=self.hl.start_task, args=(self.keysword,))
        self.thread.start()
        self.hl.show_data.connect(self.show_d)

    def show_d(self, value):
        # self.textEdit.clear()
        # print(value)
        # con = '\n'.join(value)
        # self.textEdit.setText(con)
        self.textEdit.append(value)

    def save_file(self):
        print("save_file")
        data_str = self.textEdit.toPlainText()
        data_list = data_str.split('\n')
        if os.path.exists(self.keysword + '.csv'):
            os.remove(self.keysword + '.csv')
        for data in data_list:
            with open(self.keysword + '.csv', 'a', encoding='utf-8-sig', newline='') as file:
                writer = csv.writer(file, dialect='excel')
                writer.writerow([data])
        print('酒店保存成功!!!')
        self.showMessage()
        # self.thread = threading.Thread(target=self.xc.start_task, args=(data,))
        # self.thread.start()

    def quit_sys(self):
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
