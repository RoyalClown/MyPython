import os
import random
import urllib.request

import requests

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.OracleConnection import OracleConnection
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class ImgDownload:
    def __init__(self):
        self.path = "I:\PythonPrj\StandardSpider\\tmp\\"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.db = OracleConnection()

    def write(self):
        with open(self.path + "text.txt", 'w') as f:
            f.write('aaa')

    def get_urls_from_db(self):
        cursor = self.db.conn.cursor()
        # 去除与之前爬取img重复的

        cursor.execute("update product$component set cmp_img=null where cmp_img='None'")
        cursor.execute(
            "update product$component_crawl a set cc_b2c_img=(select cc_b2c_img from product$component_crawl b where a.cc_img=b.cc_img and b.cc_b2c_img is not null and rownum=1) where cc_b2c_img is null")
        cursor.execute("select distinct cc_img from product$component_crawl where cc_b2c_img is null and cc_img is not null")
        img_datas = cursor.fetchall()
        cursor.close()
        self.db.conn.commit()
        self.db.conn.close()

        img_urls = []
        for img_data in img_datas:
            img_urls.append(img_data[0])
        return img_urls

    def download(self, img_url):
        filename = self.path + str(random.random()) + '.jpg'
        html_analyse = HtmlAnalyse(img_url)
        html_analyse.download(filename)
        print("下载完成。。。")
        return filename

    def upload(self, filename, img_url):
        try:
            with open(filename, 'rb') as file:
                res = requests.post("http://10.10.100.200:9999/file/upload", files={'file': file})
                res_j = res.json()
            db = OracleConnection()
            cursor = db.conn.cursor()
            cursor.execute(
                "update product$component_crawl set cc_b2c_img='{}' where cc_img='{}'".format(res_j['path'],
                                                                                              img_url))
            print("上传并更新完成")
            cursor.close()
            db.conn.commit()
            db.conn.close()
        except Exception as e:
            print(e)

    def go(self):
        img_urls = self.get_urls_from_db()
        for img_url in img_urls:
            filename = self.download(img_url)
            self.upload(filename, img_url)

    def thread_go(self):
        img_urls = self.get_urls_from_db()

        def thread(imgurl):
            filename = self.download(imgurl)
            self.upload(filename, imgurl)

        threading_pool = ThreadingPool()
        threading_pool.multi_thread(thread, img_urls)


if __name__ == "__main__":
    imgdownload = ImgDownload()
    # imgdownload.go()

    imgdownload.thread_go()
