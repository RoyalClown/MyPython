"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/16
"""
import json
import re

import requests
from bs4 import BeautifulSoup

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Yageo.YageoConstant import Yageo_Pre_Pdf_Url


class ProductList:
    def __init__(self,
                 url="http://www.yageo.com/NewPortal/_cn/search/search-1-1.jsp"):
        self.url = url

    def get_product_list(self):
        html_analyse = HtmlAnalyse(self.url)
        data = {"Category_Radio": "Rchip", "Feature_Radio": "Rchip_HighVoltage", "CATEGORY": "Rchip",
                "FEATURE": "Rchip_HighVoltage", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        contents = html_analyse.post_contents(data=data)
        bs_contents = BeautifulSoup(contents, "html.parser")
        product_tags = bs_contents.find_all(name="tr")[1:]
        return product_tags


class Detail:
    def __init__(self, product_tag):
        self.td_tags = product_tag.find_all(name="td")

    def get_component(self):
        url = "http://www.yageo.com/NewPortal/_cn/search/search-1-1.jsp"
        code = self.td_tags[0].text
        kiname = self.td_tags[1].text

        img = ""

        rough_attach = Yageo_Pre_Pdf_Url + code
        res = requests.head(rough_attach, allow_redirects=False)
        attach = res.headers["Location"]

        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        many_attributes = []
        column_relation = {2: "Size ( Dimension)", 3: "Tolerance", 4: "T.C.R", 5: "Rated Power",
                           6: "Resistance Value"}
        for det_no, key in column_relation.items():
            rough_value = self.td_tags[det_no].text
            if key == "Size ( Dimension)":
                value = re.compile(r'\(.*\)').sub("", rough_value)
            elif key == "Rated Power":
                try:
                    value = re.match(r'.*?\((.*?)\)', rough_value).group(1)
                except:
                    value = rough_value
            else:
                value = rough_value
            attribute = (key, value)
            many_attributes.append(attribute)

        return many_attributes


if __name__ == "__main__":
    productlist = ProductList()
    data_json = productlist.get_product_list()
    print(data_json)
