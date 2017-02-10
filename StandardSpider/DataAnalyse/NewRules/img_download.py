import os
import random
import urllib.request

import requests

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.OracleConnection import OracleConnection
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class ImgDownload:
    def __init__(self, task_code):
        self.task_code = task_code
        self.path = "C:\img\\"
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
            "merge into product$component_crawl a using ( select cc_b2c_img,cc_img from product$component_crawl where cc_b2c_img is not null group by cc_b2c_img,cc_img ) b on (a.cc_img = b.cc_img ) when matched then update set a.cc_b2c_img = b.cc_b2c_img where a.cc_b2c_img is null")
        cursor.execute("select distinct cc_img from product$component_crawl where cc_b2c_img is null and cc_img is not null and cc_task=(select cct_id from product$component_crawl_task where cct_taskid='{}')".format(self.task_code))
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
    task_code = input("请输入任务号:")
    imgdownload = ImgDownload(task_code)
    # imgdownload.go()

    imgdownload.thread_go()
