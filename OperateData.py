import csv
import os
import pymssql
import pymysql
import time
from PyQt5.QtCore import QThread, pyqtSignal


class APIList(object):
    SERVER = "106.54.85.99"
    USER = 'MH23User'
    PWD = '8ju4G$lhkwjq#yQT'
    DataBase = "MH23DB"
    Port = 61235


class OperateSql(QThread):
    """携程数据增删查询"""
    show_bar = pyqtSignal(int)
    show_data = pyqtSignal(list)
    show_num = pyqtSignal(list)

    def __init__(self, parent=None):
        super(OperateSql, self).__init__(parent=parent)
        self.db = pymysql.connect(host='47.92.162.87', port=3306, user='root', password='ershi123',
                                  db='db_bby_xiecheng')
        self.cursor = self.db.cursor()
        self.data_list = []
        if os.path.exists(r'携程酒店.csv'):
            with open(r'携程酒店.csv', 'r', newline='', encoding='gbk') as file:
                reader = csv.reader(file)
                for row in reader:
                    # print(row[0])
                    hotel_name = row[0].strip()
                    self.data_list.append(hotel_name)
        else:
            print('携程酒店.csv文件不存在!!!')

    def read_excel(self):
        """读取excel数据, 并清空数据库"""
        # print(self.data_list)
        delete_sql = 'truncate table t_cl_xiecheng_hotel'
        self.cursor.execute(delete_sql)
        self.insert_sql(self.data_list)

    def insert_sql(self, data_list):
        """更新酒店数据"""
        total_len = len(data_list)
        step = 0
        for hotel in data_list:
            update_sql = 'insert into t_cl_xiecheng_hotel (hotel) values ("%s")' % hotel
            try:
                self.cursor.execute(update_sql)
                self.db.commit()
                print(hotel)
            except Exception as e:
                print(e)
                self.db.rollback()
                print('数据更行失败!!!')
            step += 100 / int(total_len)
            self.show_bar.emit(step)
        self.show_bar.emit(100)

    def select_sql(self):
        """查询数据"""
        while True:
            with pymssql.connect(APIList.SERVER, APIList.USER, APIList.PWD, APIList.DataBase,
                                 port=APIList.Port) as conn:
                with conn.cursor() as cursor:
                    select_num = 'select max(pici) from hotel'
                    hotel_sql = 'select count(hotel_name) from hotel where pici = (select max(pici) from hotel)'
                    # select_num = 'select count(hotel_name) from hotel_xiecheng order by pici desc limit 0,1'
                    cursor.execute(select_num)
                    result = cursor.fetchone()
                    max_num = result[0]
                    cursor.execute(hotel_sql)
                    result = cursor.fetchone()
                    hotel_num = result[0]
                    data_sql = 'select hotel_name from hotel where pici=%s' % max_num
                    # print(data_sql)
                    cursor.execute(data_sql)
                    result = cursor.fetchall()
                    data_num = list(map(lambda x: x[0], result))
                    print(max_num)
                    print(hotel_num)
                    print(data_num)
                    self.show_num.emit([max_num, hotel_num])
                    self.show_data.emit(data_num)
            time.sleep(60)

    def start_task(self):
        self.start()

    def run(self):
        self.select_sql()
        # self.read_excel()


if __name__ == "__main__":
    op = OperateSql()
    op.run()
