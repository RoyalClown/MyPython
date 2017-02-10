"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/29
"""
import json
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.ST.STConstant import ST_Pre_Url


class ProductList:
    def __init__(self,
                 url="http://www.st.com/content/st_com/en/products/automotive-logic-ics/gates.html?querycriteria=productId=SC1799"):
        self.url = url

    def get_product_list(self):
        res = requests.get(
            "http://www.st.com/content/st_com/en/products/automotive-logic-ics/gates.product-grid.html/SC1799.json")
        contents = res.content.decode("utf-8")

        data_json = json.loads(contents)
        return data_json["rows"]


class Detail:
    def __init__(self, data_json):
        self.product_json = data_json

    def get_component(self):
        url = ST_Pre_Url + self.product_json["productFolderUrl"]
        code = self.product_json["cells"][0]["value"]
        kiname = "Gates"

        img = ""

        def get_attach(detail_url):
            html_analyse = HtmlAnalyse(detail_url)
            bs_content = html_analyse.get_bs_contents()
            rough_attach = bs_content.find(name="a", id="displayedPath")
            try:
                attach = ST_Pre_Url + rough_attach.get("href")
            except:
                attach = ""
            return attach

        attach = get_attach(url)
        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        attributes_values = self.product_json["cells"]

        attributes_list = ["Part Number", "General Description", "Fabrication Technology", "Marketing Status",
                           "Package", "Supply Voltage (V)min", "Supply Voltage (V)max", "Vi Range",
                           "Operating Temperature (°C)min", "Operating Temperature (°C)max"]
        many_attributes = []
        for attribute_value, attribute_name in zip(attributes_values[1:], attributes_list[1:]):
            attribute = (attribute_name, attribute_value["value"],)
            many_attributes.append(attribute)
        return many_attributes

if __name__ == "__main__":
    productlist = ProductList()
    data_json = productlist.get_product_list()
    print(data_json)