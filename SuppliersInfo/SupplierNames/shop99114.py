"""
    @description:
    @author:        RoyalClown
    @date:          2017/2/21
"""

import re

from pymongo import MongoClient

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class Shop99114:
    def __init__(self):
        conn = MongoClient("10.10.101.22", 27017)
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
            company_tags = bs_content.find_all(name="a", attrs={"target": "_blank", "href": re.compile(r"/\d+")})
            corporations = []
            for company_tag in company_tags:
                corporation = company_tag.text.strip()
                corporation_dict = {"corporation": corporation, "province_url": city_url, "page_url": page_url,
                                    "状态": "未完成", "from": "99114"}
                corporations.append(corporation)
                col = self.db.All_Company_Name
                col.insert(corporation_dict)
            print(corporations)
            return corporations

        html_analyse = HtmlAnalyse("http://shop.99114.com/")
        bs_content = html_analyse.get_bs_contents()
        all_city_tags = bs_content.find_all(name="a", attrs={"href": re.compile(r"http://shop\.99114\.com/list/area")})
        for city_tag in all_city_tags:
            city_url = city_tag.get("href")
            html_analyse = HtmlAnalyse(city_url)
            bs_content = html_analyse.get_bs_contents()
            page_tag = bs_content.find_all(name="a", attrs={"href": re.compile(r"/list/area/")})[-2]
            page_count = int(page_tag.text.replace(",", ""))
            page_urls = map(lambda page_num: city_url[:-1] + str(page_num) + ".html",
                            range(1, page_count + 1))

            # for page_url in page_urls:
            #     thread_go(page_url)

            threading_pool = ThreadingPool(12)
            threading_pool.multi_process(thread_go, page_urls)

            # 企业详情页信息获取


if __name__ == "__main__":
    supplierlist = Shop99114()
    supplierlist.get_suppliers()
