import ctypes
import inspect
import sys
import threading

from PyQt5.QtWidgets import QMainWindow, QApplication

from SeleniumNew import XieChenGSpider
from window import Ui_MainWindow


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ui()
        self.setWindowTitle('携程酒店')

    def init_ui(self):
        self.xc = XieChenGSpider()
        self.xc.show_num.connect(self.show_num)
        self.xc.show_hotel_num.connect(self.show_hotel_num)
        self.xc.show_data.connect(self.show_d)
        self.pushButton.clicked.connect(self.start_1)
        self.pushButton_2.clicked.connect(self.quit_sys)

    def show_hotel_num(self, value):
        self.lineEdit_4.setText(str(value))

    def show_num(self, value):
        self.lineEdit_3.setText(str(value))

    def show_d(self, value):
        self.textEdit.append(value)

    def start_1(self):
        data = {}
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        data['username'] = username
        data['password'] = password
        self.thread = threading.Thread(target=self.xc.start_task, args=(data,))
        self.thread.start()

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
