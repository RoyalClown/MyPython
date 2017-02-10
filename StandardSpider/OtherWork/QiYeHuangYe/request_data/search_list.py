import json
import re
import socket

import requests
import time

from pymongo import MongoClient

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.Proxy_Pool import ProxyPool
from OtherWork.QiYeHuangYe.request_data.Constant import TianYan_Headers, TianYan_Cookies


class SearchList:
    def __init__(self):
        self.proxy_pool = ProxyPool()
        self.proxy_ip = self.proxy_pool.get()
        self.page_count = ""

    def get_all_urls(self, key_word):
        while True:
            my_session = requests.session()
            my_session.headers.update(TianYan_Headers)
            my_session.proxies.update(self.proxy_ip)
            try:
                first_res = my_session.get("http://www.tianyancha.com/tongji/" + key_word + ".json?random=" + str(
                        round(time.time(), 3)).replace(".", ""))
                first_content = first_res.content
                first_data_v = eval(first_content)["data"]["v"]
            except Exception as e:
                print(e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()

                continue
            if first_res.status_code != 200 or not first_content:
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            first_token = re.match(r".*?token=(.*?);.*?", str(bytes(eval(first_data_v)))).group(1)

            my_cookie = TianYan_Cookies

            my_cookie["token"] = first_token

            my_session.cookies.update(my_cookie)
            try:
                real_res = my_session.get("http://www.tianyancha.com/search/" + key_word + ".json?")

                content = real_res.content.decode()
            except Exception as e:
                print(e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            if first_res.status_code != 200 or not content:
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            break
        conn = MongoClient()
        try:
            json_list = json.loads(content)
        except Exception as e:
            print(e)
            return
        brief_companies = json_list["data"]
        if not brief_companies:
            print(key_word, "无数据")
            col = conn.spider.Company_Name_Test
            col.update({"corporation": key_word}, {'$set': {"状态": "无数据"}}, multi=True, upsert=True)
            conn.close()
            return

        for brief_company in brief_companies:
            company_id = brief_company["id"]
            detail_company_url = "http://www.tianyancha.com/company/" + str(company_id)
            detail_company = {"company_id": company_id, "url": detail_company_url, "状态": "未完成"}
            detail_col = conn.spider.Company_Info
            detail_col.insert(detail_company)
        col = conn.spider.Company_Name_Test
        col.update({"corporation": key_word}, {'$set': {"状态": "已完成"}}, multi=True, upsert=True)
        print(key_word, "已完成")
        conn.close()
# 470

if __name__ == "__main__":
    socket.setdefaulttimeout(30)
    mongo_conn = MongoClient()
    col = mongo_conn.spider.All_Company_Name
    search_list = SearchList()
    key_words = []
    for data in col.find({"状态": "未完成"}):
        key_word = data["corporation"]
        key_words.append(key_word)

    threadingpool = ThreadingPool()
    threadingpool.multi_thread(search_list.get_all_urls, key_words)
