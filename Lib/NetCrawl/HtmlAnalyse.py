import gzip
import json

import sys
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from selenium.webdriver import DesiredCapabilities

from Lib.NetCrawl.Constant import Default_Header


class HtmlAnalyse:
    def __init__(self, url, proxy=None, is_cookie=False):
        self.url = url
        self._session = requests.Session()
        self._session.headers.update(Default_Header)
        if proxy:
            self._session.proxies.update(proxy)


        if is_cookie:
            with open("I:\PythonPrj\StandardSpider\Lib\\NetCrawl\Cookie.json") as f:
                cookies = f.read()
            print(cookies)
            cookies_dict = json.loads(cookies)
            self._session.cookies.update(cookies_dict)

    # 获得页面内容
    def get_contents(self):
        res = self._session.get(self.url, timeout=30)
        if res.status_code == 200:
            contents = res.text
            return contents
        else:
            print("网页状态码：%d" % res.status_code)
            return None

    # 模拟浏览器获得内容
    def get_selenium_contents(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"]=("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36")

        driver = webdriver.PhantomJS(
            executable_path='C:\\Users\\RoyalClown\\Desktop\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe', desired_capabilities=dcap)
        try:
            driver.get(self.url)
            contents = driver.page_source
            driver.quit()
            return contents
        except Exception as e:
            print(sys._getframe().f_code.co_name, e)
            self.get_selenium_contents()

    # 获得bs对象
    def get_bs_contents(self):
        bs_contents = BeautifulSoup(self.get_contents(), "lxml")
        return bs_contents

    # 模拟浏览器获得bs对象
    def get_selenium_bs_contents(self):
        bs_contents = BeautifulSoup(self.get_selenium_contents(), "html.parser")
        return bs_contents

    # 解压文本
    def explode(self):
        content = self.get_contents()
        try:  # 尝试解压
            print('正在解压.....')

            content = gzip.decompress(content)
            print('解压完毕!')
        except:
            print('未经压缩, 无需解压')
        return content

    # 下载文件
    def download(self, path):
        res = self._session.get(self.url, stream=True, timeout=30, verify=False)
        if not res.content or res.status_code != 200:
            raise EOFError

        with open(path, 'wb') as f:
            f.write(res.content)

    def post_download(self, path, data):
        res = self._session.post(self.url, data=data, stream=True, timeout=30)
        with open(path, 'wb') as f:
            f.write(res.content)

    def post_contents(self, data):
        contents = self._session.post(self.url, data=data).text
        return contents


if __name__ == "__main__":
    while True:
        html_analyse = HtmlAnalyse("http://www.digikey.com.cn/search/zh?site=cn&lang=zh")
        bs_content = html_analyse.get_bs_contents()
        print(bs_content)
