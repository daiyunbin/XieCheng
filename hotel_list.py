import random
import requests
import time
from PyQt5.QtCore import QThread, pyqtSignal


class HotelList(QThread):
    show_data = pyqtSignal(str)
    HotelURL = 'https://m.ctrip.com/restapi/h5api/globalsearch/search?action=online&source=globalonline&keyword={}'

    def __init__(self, parent=None):
        super(HotelList, self).__init__(parent=parent)
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        }

        # 获取酒店url

    def get_url(self, hotel_name):
        """根据酒店名，获取酒店url"""
        info_url = HotelList.HotelURL.format(hotel_name)
        try:
            resp = requests.get(info_url, headers=self.headers)
            if resp.status_code == 200:
                hotel_list = resp.json()['data']
                for hotel in hotel_list:
                    name = hotel.get("word")
                    print(name)
                    self.show_data.emit(name)

            else:
                print(resp.status_code)
                print('获取节点页面服务器响应错误!!!')
                time.sleep(random.uniform(0.8, 1.2))
                self.get_url(hotel_name)
        except Exception as e:
            print(e)
            print('获取酒店页面url服务器错误!!!')
            self.get_url(hotel_name)
            time.sleep(random.uniform(0.8, 1.2))

    def run(self):
        self.get_url(self.keyword)
        self.show_data.emit("已完成!!!")

    def start_task(self, keyword):
        self.keyword = keyword
        self.start()


if __name__ == "__main__":
    hl = HotelList()
    hl.get_url("悦来客栈")
