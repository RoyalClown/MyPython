"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/9
"""
import json
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Infineon.InfineonConstant import Infineon_Pre_Url


class ProductList:
    def __init__(self,
                 url="http://www.infineon.com/cms/cn/product/power/power-mosfet/500v-900v-n-channel-coolmos-power-mosfet/600v-coolmos-n-channel-power-mosfet/channel.html?channel=ff80808112ab681d0112ab6a628704d8"):
        self.url = url

    def get_product_list(self):
        html_analyse = HtmlAnalyse(self.url)
        bs_contents = html_analyse.get_bs_contents()
        rough_products = bs_contents.find_all(name="tr", attrs={"class": "products"})
        products_urls = []
        for rough_product in rough_products:
            url = Infineon_Pre_Url + rough_product.td.a.get("href")
            products_urls.append(url)
        return products_urls


class Detail:
    def __init__(self, product_url):
        self.url = product_url
        html_analyse = HtmlAnalyse(self.url)
        self.bs_content = html_analyse.get_bs_contents()

    def get_component(self):
        url = self.url
        try:
            code = self.bs_content.find(name="th", text='OPN').next_sibling.next_sibling.text
        except:
            code = self.bs_content.find(name="h1", attrs={"class": "page-title"}).text
        kiname = "800V CoolMOS™ N-Channel Power MOSFET"
        img = ""
        data_sheet = self.bs_content.find(name="a", attrs={"href": re.compile(r'/dgdl/Infineon.*?EN\.pdf')})
        attach = Infineon_Pre_Url + data_sheet.get("href")
        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        many_attributes = []
        trs = self.bs_content.find_all(name="tr", attrs={"class": "table-header gradient checker-dotted"})
        for tr in trs:
            if tr.th:
                key = tr.th.text
                value = tr.td.text.strip()
            elif tr.td:
                if "R" in tr.td.text and "DS (on)" in tr.td.text and "max" in tr.td.text:
                    key = "RDS (on) max"
                    value = tr.td.next_sibling.next_sibling.text.strip()
                elif "R" in tr.td.text and "DS (on)" in tr.td.text:
                    key = "RDS (on)"
                    value = tr.td.next_sibling.next_sibling.text.strip()

                elif "Operating Temperature" in tr.td.text and "min" in tr.td.text and "max" in tr.td.text:
                    key = "Operating Temperature min max"
                    value = tr.td.next_sibling.next_sibling.text.strip()
                elif "Operating Temperature" in tr.td.text and "min" in tr.td.text:
                    key = "Operating Temperature min"
                    value = tr.td.next_sibling.next_sibling.text.strip()

                elif "V" in tr.td.text and "DS" in tr.td.text and "max" in tr.td.text:
                    key = "VDS max"
                    value = tr.td.next_sibling.next_sibling.text.strip()
                elif "V" in tr.td.text and "DS" in tr.td.text:
                    key = "VDS"
                    value = tr.td.next_sibling.next_sibling.text.strip()

                elif "V" in tr.td.text and "GS(th)" in tr.td.text and "min" in tr.td.text and "max" in tr.td.text:
                    key = "VGS(th) min max"
                    value = re.compile(r'\s').sub("", tr.td.next_sibling.next_sibling.text).replace("\xa0", "-")

                elif "Technology" in tr.td.text:
                    key = "Technology"
                    value = tr.td.next_sibling.next_sibling.text.strip()
                elif "Die Size" in tr.td.text and "(X)" in tr.td.text:
                    key = "Die Size (X)"
                    value = tr.td.next_sibling.next_sibling.text.strip()
                elif "Die Size" in tr.td.text and "(Y)" in tr.td.text:
                    key = "Die Size (Y)"
                    value = tr.td.next_sibling.next_sibling.text.strip()
                elif "I" in tr.td.text and "D" in tr.td.text and "max" in tr.td.text:
                    key = "ID max"
                    value = tr.td.next_sibling.next_sibling.text.strip()
                elif "P" in tr.td.text and "tot" in tr.td.text and "max" in tr.td.text:
                    key = "Ptot max"
                    value = tr.td.next_sibling.next_sibling.text.strip()

                elif "Q" in tr.td.text and "G" in tr.td.text:
                    key = "QG"
                    value = tr.td.next_sibling.next_sibling.text.strip()

                else:
                    key = re.compile(r'\s').sub("", tr.td.text)
                    value = re.compile(r'\s').sub("", tr.td.next_sibling.next_sibling.text)
            else:
                continue
            attribute = (key, value)
            many_attributes.append(attribute)

        return many_attributes


if __name__ == "__main__":
    productlist = ProductList()
    data_json = productlist.get_product_list()
    print(data_json)
