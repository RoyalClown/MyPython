"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/6
"""
import re

import requests
import sys

from bs4 import BeautifulSoup

from Components.DBSAVE.oracleSave import OracleSave
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.Constant import Default_Header
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class NewarkGo:
    def __init__(self):
        # self.proxy_pool = ProxyPool()
        # self.proxy_ip = self.proxy_pool.get()
        pass

    def thread_go(self, page_properties):
        first_category_name, second_category_name, page_url = page_properties
        detail_headers = Default_Header
        detail_headers["host"] = "cn.element14.com"
        detail_headers["Upgrade-Insecure-Requests"] = "1"
        while True:
            try:
                # self.proxy_ip = self.proxy_pool.get()
                detail_session = requests.session()
                detail_session.headers.update(detail_headers)
                # detail_session.proxies.update(self.proxy_ip)quoted string not properly terminated

                res = detail_session.get(page_url, timeout=20)
                if res.status_code != 200:
                    print(res.status_code)
                    # self.proxy_pool.remove(self.proxy_ip)
                    continue
                bs_content = BeautifulSoup(res.content, "lxml")
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                # self.proxy_pool.remove(self.proxy_ip)
        try:
            component_tags = bs_content.find(name="tbody").find_all(name="tr")
        except Exception as e:
            print("component_tags", e)
            return
        for component_tag in component_tags:
            td_tags = component_tag.find_all(name="td")
            try:
                component_code = td_tags[1].text.strip()
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                continue
            try:
                component_img = td_tags[1].find(name="img", attrs={"class": "productThumbnail"}).get("src")
            except:
                component_img = ""
            try:
                rough_attach = td_tags[2].find(name="a", text="数据表")
                if not rough_attach:
                    rough_attach = td_tags[2].find(name="a", attrs={"class": "prodDetailsAttachment"})
                component_attach = rough_attach.get("href")
                if "http" not in component_attach:
                    component_attach = ""
            except Exception as e:
                print("component_attach is null!!")
                component_attach = ""
            try:
                manufacture_description = td_tags[3].a.find_all(name="p")
                component_brand = manufacture_description[0].text.strip()
                component_description = manufacture_description[1].text.strip()
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                continue

            component = (
            component_code, component_brand, first_category_name, second_category_name, page_url, component_attach,
            component_img)

            count = 0
            while True:
                try:
                    orcl_conn = OracleSave(1000004)
                    orcl_conn.component_insert(component)
                    orcl_conn.commit()
                    orcl_conn.conn.close()

                    break
                except Exception as e:
                    print(e)
                    count += 1
                    if count > 3:
                        break

    def get_category_url(self):
        my_headers = Default_Header
        my_headers["host"] = "cn.element14.com"
        my_headers["Upgrade-Insecure-Requests"] = "1"
        while True:
            try:
                # self.proxy_ip = self.proxy_pool.get()
                my_session = requests.session()

                my_session.headers.update(Default_Header)
                # my_session.proxies.update(self.proxy_ip)

                res = my_session.get("http://cn.element14.com/browse-for-products", timeout=20)
                if res.status_code != 200:
                    print(res.status_code)
                    # self.proxy_pool.remove(self.proxy_ip)
                    continue
                bs_content = BeautifulSoup(res.content, "lxml")
                first_category_tags = bs_content.find_all(name="ul", attrs={"categoryList"})
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                # self.proxy_pool.remove(self.proxy_ip)
        pages_properties = []
        for first_category_tag in first_category_tags[-2:-1]:
            first_category_name = first_category_tag.li.h2.text.strip()
            second_category_tags = first_category_tag.li.ul.find_all(name="li")
            for second_category_tag in second_category_tags:
                second_category_url = second_category_tag.a.get("href")
                rough_second_category_name = second_category_tag.text.strip()
                flag = re.match(r"(.*?) \((\d+.*?)\)", rough_second_category_name)
                second_category_name = flag.group(1)
                component_count = flag.group(2).replace(",", "")
                if component_count == '1':
                    continue
                page_count = int(int(component_count) / 25) + 1

                for page_num in range(1, page_count + 1):
                    page_url = second_category_url + "/prl/results/" + str(page_num)
                    page_properties = (first_category_name, second_category_name, page_url)
                    pages_properties.append(page_properties)

        return pages_properties

    def newark_go(self):
        pages_properties = self.get_category_url()

        for page_properties in pages_properties:
            self.thread_go(page_properties)

        # threadingpool = ThreadingPool(20)
        # threadingpool.multi_thread(self.thread_go, pages_properties)

if __name__ == "__main__":
    newark_go = NewarkGo()
    newark_go.newark_go()
