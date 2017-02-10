"""
    @description:   
    @author:        RoyalClown
    @date:          2016/1/11
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
        data = {"Category_Radio": "Rchip", "Feature_Radio": "Rchip_Automotive", "CATEGORY": "Rchip",
                "FEATURE": "Rchip_Automotive", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        contents = html_analyse.post_contents(data=data).encode().decode()
        bs_contents = BeautifulSoup(contents, "html.parser")
        product_tags = bs_contents.find_all(name="tr")[1:]
        return product_tags


class Detail:
    def __init__(self, product_tag):
        self.td_tags = product_tag.find_all(name="td")

    def get_component(self):
        code = self.td_tags[0].text

        attach = Yageo_Pre_Pdf_Url + code
        component = [attach, ]
        for det_no in range(7):
            value = self.td_tags[det_no].text.replace("Â", "").replace(",", " ")
            component.append(value)

        return component


if __name__ == "__main__":
    productlist = ProductList()
    product_tags = productlist.get_product_list()
    with open("../CCT2017011600000033.csv", "w", encoding="utf-8") as f:
        f.write(
            "pdf, Part No.,Series Name,Size ( Dimension),Tolerance,T.C.R,Rated Power,Resistance Value\n")
        for product_tag in product_tags:
            detail = Detail(product_tag)
            component = detail.get_component()
            print(component)
            line = (",".join(component)) + "\n"
            f.write(line.encode().decode())
