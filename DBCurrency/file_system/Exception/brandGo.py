"""
    @description:   
    @author:        RoyalClown
    @date:          2017/5/8
"""
import os
import random

import cx_Oracle
import sys

import requests

from DBCurrency.file_system.FileSystemConstant import File_Server_Url
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.DBConnection.Constant import B2B_Oracle_Url
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class BrandGo:
    def __init__(self):
        pass

    def get_download_urls(self):
        oracle_conn = cx_Oracle.connect(B2B_Oracle_Url)
        cursor = oracle_conn.cursor()
        sql_sentence = "select br_id, br_logourl from product$brand_import where br_logourl is not null and br_logourl_c is null"
        cursor.execute(sql_sentence)
        brand_logo_urls = cursor.fetchall()
        cursor.close()
        oracle_conn.close()
        return brand_logo_urls

    def update_local_url(self, server_file_url, br_id):
        oracle_conn = cx_Oracle.connect(B2B_Oracle_Url)
        cursor = oracle_conn.cursor()
        sql_sentence = "update product$brand_import set br_logourl_c='{}' where br_id={}".format(server_file_url, br_id)
        cursor.execute(sql_sentence)
        print("Update Success !!")
        cursor.close()
        oracle_conn.commit()
        oracle_conn.close()


class DownloadUpload:
    def __init__(self):
        self.proxy_pool = ProxyPool()
        self.proxy_ip = self.proxy_pool.get()
        pass

    def file_download(self, url, file_type, file_name=str(random.random())):
        download_dir_path = "..\\download_files\\"
        if not os.path.exists(download_dir_path):
            os.mkdir(download_dir_path)
        download_file_path = download_dir_path + file_name + file_type
        if os.path.exists(download_file_path):
            return
        try_count = 0
        while True:
            try:
                download_file_path = download_dir_path + str(random.random()) + file_type
                # html_analyse = HtmlAnalyse(url, proxy=self.proxy_ip)
                my_session = requests.session()
                my_headers = {'Connection': 'Keep-Alive',
                              'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'Accept-Encoding': 'gzip, deflate, sdch',
                              "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                              "host": "www.newark.com", "Referer": "http://www.newark.com/",
                              "Upgrade-Insecure-Requests": "1"}
                my_session.headers.update(my_headers)
                my_session.proxies.update(self.proxy_ip)
                res = my_session.get(url)
                if res.status_code != 200 or not res.content:
                    print(sys._getframe().f_lineno)
                    continue
                with open(download_file_path, 'wb') as f:
                    f.write(res.content)

                print("File Download Success !!")
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, url, e)
                try_count += 1
                # if try_count > 2 and "https" in url:
                #     return
                # if try_count > 5:
                #     return
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                # download_file_path = download_dir_path + str(random.random()) + file_type

        return download_file_path

    def file_upload(self, local_file_path):
        if not local_file_path:
            return
        while True:
            try:
                with open(local_file_path, "rb") as f:
                    res = requests.post(File_Server_Url, files={'file': f})
                    if res.status_code == 200:
                        res_j = res.json()
                        break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
        server_file_path = res_j["path"]
        print("File Server Upload Success !!")
        return server_file_path

    def download_upload(self, url, file_type):
        download_file_path = self.file_download(url, file_type)
        server_file_path = self.file_upload(download_file_path)
        return server_file_path


if __name__ == "__main__":
    def thread_go(brand_logo_url):
        br_id, logo_url = brand_logo_url

        if "newark" not in logo_url:
            return
        server_file_url = download_upload.download_upload(logo_url, ".png")
        if server_file_url:
            brand_go.update_local_url(server_file_url, br_id)


    brand_go = BrandGo()
    brand_logo_urls = brand_go.get_download_urls()

    download_upload = DownloadUpload()
    for brand_logo_url in brand_logo_urls:
        thread_go(brand_logo_url)

    # threadingpool = ThreadingPool(4)
    # threadingpool.multi_thread(thread_go, brand_logo_urls)


        # def brand_logo_go(self):
        #     def thread_go(brand_logo_url):
        #         br_id, logo_url = brand_logo_url
        #
        #         if "smhttp" in logo_url:
        #             return
        #         server_file_url = file_system.download_upload(logo_url, ".png")
        #         if server_file_url:
        #             self.update_local_url(server_file_url, br_id)
        #
        #     brand_logo_urls = self.get_download_urls()
        #     file_system = FileSystem()
        #
        #     # threadingpool = ThreadingPool(20)
        #     # threadingpool.multi_thread(thread_go, brand_logo_urls)
        #
        #     for brand_logo_url in brand_logo_urls:
        #         thread_go(brand_logo_url)
