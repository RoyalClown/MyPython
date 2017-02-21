"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/14
"""
import re

import requests
import time

import sys
from bs4 import BeautifulSoup

from Components.MLCC1.Constant import First_Headers, First_Cookies, Pre_Url
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class MLCC1Detail:
    def __init__(self, second_class):
        self.first_class_name, self.second_class_name, self.url, self.page_count = second_class
        self.proxy_pool = ProxyPool()

        self.proxy_ip = self.proxy_pool.get()

    def get_class_components(self):
        page_urls = map(lambda num: self.url + "&p=" + str(num), range(1, self.page_count + 1))

        return page_urls

    def get_page_components(self, page_url):
        my_headers = First_Headers
        my_cookies = First_Cookies
        my_session = requests.session()
        my_session.headers.update(my_headers)
        my_session.cookies.update(my_cookies)
        while True:
            try:
                my_session.proxies.update(self.proxy_ip)
                pass
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                time.sleep(1)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
            try:
                res = my_session.get(page_url, timeout=15)
                content = res.content.decode()
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue

            if res.status_code == 200 and content:
                break
            else:
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()

        bs_content = BeautifulSoup(content, "lxml")
        product_tags = bs_content.find_all(name="li", attrs={"data-id": re.compile(r'\d+')})

        many_components_properties = []
        for product_tag in product_tags:
            all_p_tags = product_tag.find_all(name="p")
            product_code = all_p_tags[0].b.a.text

            product_brand = all_p_tags[0].span.text

            product_parameter = all_p_tags[0].find(name="a", id="params").text
            try:
                product_pdf = product_tag.find(name="a", attrs={"data-id": "pdf"}).get("href")
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                product_pdf = ""
            if "http://" not in product_pdf:
                product_pdf = Pre_Url + product_pdf

            component = (product_code, product_pdf, "null", product_brand, self.first_class_name, self.second_class_name, page_url)

            properties = [("product_parameter", product_parameter), ]
            try:
                product_details = all_p_tags[3].find_all(name="span")
            except Exception as e:
                print(e)
                product_details = ""
            for product_detail in product_details:
                detail_text = product_detail.text.split("：")
                try:
                    key_value = (detail_text[0], detail_text[1])
                except Exception as e:
                    print(e)
                    key_value = (detail_text[0], "")
                properties.append(key_value)
            component_properties = (component, properties)
            many_components_properties.append(component_properties)
        return many_components_properties

if __name__ == "__main__":
    detail = MLCC1Detail(('电容', 'MLCC', 'http://www.mlcc1.com/search_simple.html?searchkey=&flag=3', 20210))
    page_urls = detail.get_class_components()
    for page_url in page_urls:
        detail.get_page_components(page_url)
