import re
import socket
import sys

from pymongo import MongoClient

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Lib.NetCrawl.Proxy_Pool import ProxyPool



class SuppliersList:
    def __init__(self):
        self.proxy_pool = ProxyPool(flag=False)
        self.proxy_ip = self.proxy_pool.get()
        conn = MongoClient()
        self.db = conn.spider

    def get_suppliers(self):
        def thread_go(page_url):
            html_analyse = HtmlAnalyse(page_url)
            while True:
                try:
                    bs_content = html_analyse.get_bs_contents()
                    break
                except Exception as e:
                    print(e)
            ul_tag = bs_content.find(name="div", attrs={"class": "leftbox comlist"})
            li_tags = ul_tag.find_all(name="li")
            corporations = []
            for li_tag in li_tags:
                corporation = li_tag.text.strip()
                corporation_dict = {"corporation": corporation, "province_url": province_url, "page_url": page_url,
                                    "状态": "未完成"}
                corporations.append(corporation)
                col = self.db.All_Company_Name
                col.insert(corporation_dict)
            print(corporations)
            return corporations

        for province_id in range(1, 36):
            province_url = "http://www.soudh.com/province-" + str(province_id) + ".html"
            html_analyse = HtmlAnalyse(province_url)
            bs_content = html_analyse.get_bs_contents()
            page_tag = bs_content.find(name="span", text=re.compile(r'当前为'))
            page_count = int(re.match(r'.*?共(\d+)页', page_tag.text).group(1))
            page_urls = map(lambda page_num: province_url[:-5] + "-" + str(page_num) + ".html",
                            range(1, page_count + 1))
            #
            # for page_url in page_urls:
            #     thread_go(page_url)

            threading_pool = ThreadingPool()
            threading_pool.multi_thread(thread_go, page_urls)

            # 企业详情页信息获取


if __name__ == "__main__":
    supplierlist = SuppliersList()
    supplierlist.get_suppliers()
