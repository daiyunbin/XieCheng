import csv
import datetime
import json
import random
import pymssql
import os
import requests
import time
from lxml import etree
from PyQt5.QtCore import QThread, pyqtSignal
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

__author__ = "zyd"
__dec__ = """携程30天酒店"""


class APIList(object):
    SERVER = "106.54.85.99"
    USER = 'MH23User'
    PWD = '8ju4G$lhkwjq#yQT'
    DataBase = "MH23DB"
    Port = 61235
    # UserName = '15219443776'
    # PassWord = 'shujuzhuaqu'
    LoginURL = 'https://passport.ctrip.com/user/login'
    HotelURL = 'https://m.ctrip.com/restapi/h5api/globalsearch/search?action=online&source=globalonline&keyword={}'


class XieChenGSpider(QThread):
    show_data = pyqtSignal(str)
    show_num = pyqtSignal(int)
    show_hotel_num = pyqtSignal(int)
    Num = 1  # 批号
    LastPrice = ''

    def __init__(self, parent=None):
        super(XieChenGSpider, self).__init__(parent=parent)
        # self.__options = webdriver.ChromeOptions()
        # self.__options.add_argument('--dns-prefetch-disable')
        # self.__options.add_argument('--disable-gpu')  # 规避bug
        # self.__options.add_argument('--disable-infobars')
        # # self.__options.add_argument('--headless')
        # self.pref = {'profile.managed_default_content_settings.images': 2}
        # self.__options.add_experimental_option('prefs', self.pref)
        # self.__options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # self.driver = webdriver.Chrome(options=self.__options)
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        # 设置user-agent请求头
        dcap["phantomjs.page.settings.loadImages"] = False  # 禁止加载图片
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15, 1)

    def quit_driver(self):
        """退出浏览器"""
        self.driver.quit()

    # 获取随机请求头
    @staticmethod
    def random_user_agent():
        ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
            'Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50',
            'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
            'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11',
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
            "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        ]
        user_agent = random.choice(ua_list)
        return user_agent

    # 获取酒店url
    def get_url(self, hotel_name):
        """根据酒店名，获取酒店url"""
        info_url = APIList.HotelURL.format(hotel_name)
        headers = {'User-Agent': XieChenGSpider.random_user_agent()}
        try:
            resp = requests.get(info_url, headers=headers)
            if resp.status_code == 200:
                hotel_url = resp.json()['data'][0]['url']
                print(hotel_name + 'url:', hotel_url)
                return hotel_url
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

    # 登录
    def login_index(self, username, password):
        self.driver.get(APIList.LoginURL)
        input_user = self.wait.until(EC.presence_of_element_located((By.ID, "nloginname")))
        input_user.send_keys(username)  # 输入账号
        time.sleep(random.uniform(0.5, 0.8))
        input_pwd = self.wait.until(EC.presence_of_element_located((By.ID, "npwd")))
        input_pwd.send_keys(password)  # 输入密码
        time.sleep(random.uniform(0.5, 0.8))
        login_js = """document.querySelector("#nsubmit").click()"""
        self.driver.execute_script(login_js)
        time.sleep(random.uniform(0.5, 0.8))

    # 请求酒店页面
    def get_hotel_page(self, hotel_url):
        print('开始请求酒店主页面...')
        index_js = """window.open("{}",'_self')""".format(hotel_url)
        try:
            self.driver.execute_script(index_js)
        except Exception as e:
            print(e)
            print('主页打开失败:' + hotel_url)
        # 等待界面加载出现数据
        # self.driver.switch_to.window(self.driver.window_handles[-1])
        self.wait.until(EC.visibility_of_element_located((By.ID, "J_RoomListTbl")))
        html_page = self.driver.page_source
        today = datetime.date.today()
        if '不可取消' in html_page:
            # print('ok')
            XieChenGSpider.hotel_table(html_page)  # 存表一
            XieChenGSpider.room_table(html_page, str(today))  # 存表二
        else:
            print(hotel_url + str(today) + '没有加载开...')

        tomorrow = today + datetime.timedelta(days=1)
        for i in range(30):  # 未来30天数据
            today = tomorrow
            tomorrow = today + datetime.timedelta(days=1)
            self.update_room_date(str(today), str(tomorrow))

    # 更新酒店的住房日期
    def update_room_date(self, today, tomorrow):
        update_js = 'document.querySelector("#cc_txtCheckIn").value="{0}";' \
                    'document.querySelector("#cc_txtCheckOut").value="{1}";' \
                    'document.querySelector("#changeBtn").click()'.format(today, tomorrow)
        self.driver.execute_script(update_js)
        self.wait.until(EC.visibility_of_element_located((By.ID, "J_RoomListTbl")))
        html_page = self.driver.page_source
        if '不可取消' in html_page:
            # print('存表二')
            XieChenGSpider.room_table(html_page, today)
        else:
            print(today + '没有加载开...')

    @staticmethod
    def to_sql_room(info):
        with pymssql.connect(APIList.SERVER, APIList.USER, APIList.PWD, APIList.DataBase, port=APIList.Port) as conn:
            with conn.cursor() as cursor:
                try:
                    insert = """
                        INSERT INTO room_xiecheng(id_room_data, hotel_id,
                                    room,riqi,shifoumanfang,jiage,
                                    shangcijiage,pici,gengxingshijian) 
                                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """
                    # 从文件中读出数据
                    cursor.execute(insert,
                                   (info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8]))
                    conn.commit()
                    print('room存储成功!!!')
                except Exception as e:
                    print(e, 'room存储失败!!!')
                    print(e)
                    # cursor.close()

    @staticmethod
    def to_sql_hotel(info):
        with pymssql.connect(APIList.SERVER, APIList.USER, APIList.PWD, APIList.DataBase, port=APIList.Port) as conn:
            with conn.cursor() as cursor:
                try:
                    select_hotel = """SELECT hotel_id FROM hotel_xiecheng WHERE hotel_id=%s""" % (info[0])
                    cursor.execute(select_hotel)
                    result = cursor.fetchall()
                    # print(result)
                    if len(result) == 0:
                        insert = '''INSERT INTO hotel_xiecheng(hotel_id, hotel_name, jituan, city, shijian)
                                    VALUES (%s,%s,%s,%s,%s)'''
                        # 从文件中读出数据
                        cursor.execute(insert, (info[0], info[1], info[2], info[3], info[4]))
                        conn.commit()
                        print('hotel存储成功!!!')
                    else:
                        print('hotel已经存在...')
                except Exception as e:
                    print(e, 'hotel存储失败!!!')
                    print(info)

    # 写入表hotel表
    @staticmethod
    def hotel_table(page):
        html = etree.HTML(page)
        # 酒店id
        hotel_id = html.xpath('//a[@id="linkViewMap"]/@data-hotelid')
        hotel_id = ''.join(hotel_id)
        # 酒店名称
        hotel_name = html.xpath('//h2[@itemprop="name"]/text()')
        hotel_name = ''.join(hotel_name)
        # 集团
        jituan = html.xpath('//h2[text()="所属集团"]/following-sibling::span[1]/text()')
        jituan = ''.join(jituan)
        # 城市
        city = html.xpath('//*[@id="txtCity"]/@value')
        city = ''.join(city)
        # 时间
        shijian = str(time.strftime("%Y-%m-%d %H:%M:%S"))
        hotel_info = [hotel_id, hotel_name, jituan, city, shijian]
        print(hotel_info)
        XieChenGSpider.to_sql_hotel(hotel_info)

    # 写入roombiao
    @staticmethod
    def room_table(page, date_str):
        # 所有价格
        html = etree.HTML(page)
        all_price = html.xpath(
            '//div[@class="btns_base22_main"][not(text()="订完")]/ancestor::tr[@data-disable="0"]/td/@data-pricedisplay')
        # print(all_price)
        min_price = min(list(map(lambda x: float(x), all_price)))
        # print(min_price)
        # 酒店id
        hotel_id = html.xpath('//a[@id="linkViewMap"]/@data-hotelid')
        hotel_id = ''.join(hotel_id)
        # 房型统一基础房型
        room = '基础房'
        # 日期
        riqi = date_str
        # 是否满房
        shifoumanfang = '否'
        # 批次
        pici = str(XieChenGSpider.Num)
        # 上次价格
        shangcijiage = XieChenGSpider.LastPrice if XieChenGSpider.LastPrice else min_price
        # 更新上次价格
        XieChenGSpider.LastPrice = min_price
        # 更新时间
        gengxingshijian = str(time.strftime("%Y-%m-%d %H:%M:%S"))
        id_room_data = hotel_id + room + date_str
        room_info = [id_room_data, hotel_id, room, riqi, shifoumanfang, min_price, shangcijiage, pici, gengxingshijian]
        print(room_info)
        XieChenGSpider.to_sql_room(room_info)
        print('*' * 90)

    def start_task(self, value):
        self.value = value
        self.start()

    def run(self):
        username = self.value['username']
        password = self.value['password']
        self.login_index(username, password)  # 登录
        self.show_num.emit(XieChenGSpider.Num)
        self.driver.save_screenshot('login.png')
        while True:
            XieChenGSpider.HotelNum = 1
            print(XieChenGSpider.Num)
            self.show_num.emit(XieChenGSpider.Num)
            XieChenGSpider.Num += 1
            # hotel_name = '南京威斯汀大酒店'
            if os.path.exists(r'携程酒店.csv'):
                with open(r'携程酒店.csv', 'r', encoding='gbk') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        print(row[0])
                        hotel_name = row[0]
                        hotel_url = self.get_url(hotel_name)
                        self.get_hotel_page(hotel_url)
                        self.show_hotel_num.emit(XieChenGSpider.HotelNum)
                        self.show_data.emit(hotel_name)
                        XieChenGSpider.HotelNum += 1


if __name__ == "__main__":
    xc = XieChenGSpider()
    xc.run()
