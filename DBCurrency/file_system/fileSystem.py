"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/24
"""
import os
import random

import requests
import sys

from DBCurrency.file_system.FileSystemConstant import File_Server_Url
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class FileSystem:
    def __init__(self):
        self.proxy_pool = ProxyPool()
        self.proxy_ip = self.proxy_pool.get()

    def file_download(self, url, file_type):
        download_dir_path = "..\\download_files\\"
        if not os.path.exists(download_dir_path):
            os.mkdir(download_dir_path)
        download_file_path = download_dir_path + str(random.random()) + file_type
        while True:
            try:
                html_analyse = HtmlAnalyse(url, proxy=self.proxy_ip)
                html_analyse.download(download_file_path)
                print("File Download Success !!")
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
        return download_file_path

    def file_upload(self, local_file_path):
        with open(local_file_path, "rb") as f:
            res = requests.post(File_Server_Url, files={'file': f})
            res_j = res.json()
        server_file_path = res_j["path"]
        print("File Server Upload Success !!")
        return server_file_path

    def download_upload(self, url, file_type):
        download_file_path = self.file_download(url, file_type)
        server_file_path = self.file_upload(download_file_path)
        return server_file_path


if __name__ == "__main__":
    file_system = FileSystem()
    file_system.download_upload("https://ss1.bdstatic.com/70cFvXSh_Q1YnxGkpoWK1HF6hhy/it/u=1794894692,1423685501&fm=116&gp=0.jpg", ".jpg")