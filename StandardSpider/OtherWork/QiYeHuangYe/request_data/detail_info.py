import json
import re
import socket

import requests
import time

from pymongo import MongoClient

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.Proxy_Pool import ProxyPool
from OtherWork.QiYeHuangYe.request_data.Constant import TianYan_Detail_Headers, TianYan_Detail_Cookies


class DetailInfo:
    def __init__(self):
        self.proxy_pool = ProxyPool()
        self.proxy_ip = self.proxy_pool.get()

    def get_detail(self, url):
        while True:
            my_session = requests.session()
            my_headers = TianYan_Detail_Headers
            my_headers["Referer"] = url
            my_session.headers.update(TianYan_Detail_Headers)
            my_session.proxies.update(self.proxy_ip)

            try:
                first_res = my_session.get(url.replace("company", "tongji") + ".json?random=" + str(
                    round(time.time(), 3)).replace(".", ""))
                first_content = first_res.content
            except Exception as e:
                print(e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            if first_res.status_code != 200 or not first_content:
                print(first_res.status_code)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            first_data_v = eval(first_content)["data"]["v"]
            first_token = re.match(r".*?token=(.*?);.*?", str(bytes(eval(first_data_v)))).group(1)
            another = re.match(r".*?\{return'(.*?)'", str(bytes(eval(first_data_v)))).group(1)

            def get_wtf(another):
                data = another.split(",")
                secret = "6,b,t,f,2,z,l,5,w,h,q,i,s,e,c,p,m,u,9,8,y,k,j,r,x,n,-,0,3,4,d,1,a,o,7,v,g".split(",")
                wtf = ""
                for i in data:
                    wtf += str(secret[int(i)])
                return wtf
            first_wtf = get_wtf(another)

            my_cookie = TianYan_Detail_Cookies

            my_cookie["token"] = first_token
            my_cookie["_utm"] = first_wtf
            my_headers["CheckError"] = "check"
            my_headers["Referer"] = url

            my_session.cookies.update(my_cookie)
            my_session.headers.update(my_headers)

            try:
                real_res = my_session.get(url + ".json")

                content = real_res.content.decode()
            except Exception as e:
                print(e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            if real_res.status_code != 200 or not content:
                print(real_res.status_code)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            break
        conn = MongoClient()
        json_list = json.loads(content)
        brief_companies = json_list["data"]
        col = conn.spider.Company_Info
        if not brief_companies:
            print(url, "无数据")
            col.update({"url": url}, {'$set': {"状态": "无数据"}}, multi=True)
        else:
            col.update({"url": url}, {'$set': {"data": brief_companies, "状态": "已完成"}}, multi=True)
            print(url, "已完成")
        conn.close()

        return


if __name__ == "__main__":
    socket.setdefaulttimeout(30)
    mongo_conn = MongoClient()
    col = mongo_conn.spider.Company_Info
    detail_info = DetailInfo()

    # detail_info.get_detail("http://www.tianyancha.com/company/2546208953")
    #
    urls = []
    for data in col.find({"状态": "已完成"}):
        url = data["url"]
        urls.append(url)

    threadingpool = ThreadingPool()
    threadingpool.multi_thread(detail_info.get_detail, urls)
# Valentine's Day
