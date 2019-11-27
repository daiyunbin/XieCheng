import time
from requests_html import HTMLSession


class RequestHTML(object):
    def __init__(self):
        self.login_url = 'https://passport.ctrip.com/user/login'
        self.url = 'https://hotels.ctrip.com/hotel/346278.html'

    def get_con(self):
        """获取内容"""
        username = '15219443776'
        password = 'shujuzhuaqu'
        session = HTMLSession()
        script = """
            () => {
                    document.getElementById("nloginname").value="15219443776"
                    document.getElementById("npwd").value="shujuzhuaqu"
                    document.getElementById("nsubmit").click()
                }
        """
        r = session.get(url=self.login_url)
        dom = r.html
        dom.render(script=script)
        time.sleep(10)
        print(r.text)


if __name__ == '__main__':
    rh = RequestHTML()
    rh.get_con()
