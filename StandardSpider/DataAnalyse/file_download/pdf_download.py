import os
import random
import re


import requests

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.OracleConnection import OracleConnection
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class PdfDownload:
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
        cursor.execute("update product$component set cmp_attach=null where cmp_attach='None'")
        # 去除与之前爬取pdf重复的
        cursor.execute(
            "update product$component_crawl a set cc_b2c_attach=(select cc_b2c_attach from product$component_crawl b where a.cc_attach=b.cc_attach and b.cc_b2c_attach is not null and rownum=1) where cc_b2c_attach is null")
        cursor.execute(
            "select distinct cc_attach from product$component_crawl where cc_b2c_attach is null and cc_attach is not null")
        pdf_datas = cursor.fetchall()
        cursor.close()
        self.db.conn.commit()
        self.db.conn.close()

        pdf_urls = []
        for pdf_data in pdf_datas:
            if re.match(r'.*?\.pdf', pdf_data[0]):
                pdf_urls.append(pdf_data[0])
        return pdf_urls

    def download(self, pdf_url):
        filename = self.path + str(random.random()) + '.pdf'
        html_analyse = HtmlAnalyse(pdf_url, is_proxy=True)
        html_analyse.download(filename)
        print("下载完成。。。")
        return filename

    def upload(self, filename, pdf_url):
        try:
            with open(filename, 'rb') as file:
                res = requests.post("http://10.10.100.200:9999/file/upload", files={'file': file})
                res_j = res.json()
            print("上传完成")
            db = OracleConnection()
            cursor = db.conn.cursor()
            cursor.execute(
                "update product$component_crawl set cc_b2c_attach='{}' where cc_attach='{}'".format(res_j['path'],
                                                                                                    pdf_url))
            cursor.close()
            db.conn.commit()
            db.conn.close()

        except Exception as e:
            print(e)

    def go(self):
        pdf_urls = self.get_urls_from_db()
        for pdf_url in pdf_urls:
            filename = self.download(pdf_url)
            self.upload(filename, pdf_url)

    def thread_go(self):
        pdf_urls = self.get_urls_from_db()

        def thread(pdfurl):
            filename = self.download(pdfurl)
            self.upload(filename, pdfurl)

        threading_pool = ThreadingPool()
        threading_pool.multi_thread(thread, pdf_urls)


if __name__ == "__main__":
    pdfdownload = PdfDownload()
    # pdfdownload.upload("I:\\PythonPrj\\StandardSpider\\tmp\\0.40682021963558823.pdf", "https://industrial.panasonic.cn/cdbs/www-data/pdf/ABE0000/ABE0000C81.pdf")
    # pdfdownload.go()
    # pdfdownload.download("http://rohmfs.rohm.com/en/products/databook/datasheet/ic/memory/eeprom/br24g08-3a-e.pdf")


    pdfdownload.thread_go()

    # while True:
    #     try:
    #         pdfdownload.thread_go()
    #     except:
    #         continue
