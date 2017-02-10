"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/30
"""
import json
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.ST.STConstant import ST_Pre_Url, ST_Relation


class ProductList:
    def __init__(self,
                 url="http://www.st.com/en/interfaces-and-transceivers/smartcard-interfaces.html?querycriteria=productId=SC1620"):
        self.url = url

    def get_product_list(self):
        res = requests.get(
            "http://www.st.com/content/st_com/en/products/amplifiers-and-comparators/comparators/standard-comparators.product-grid.html/SC1620.json")
        contents = res.content.decode("utf-8")

        data_json = json.loads(contents)
        return data_json["rows"]


class Detail:
    def __init__(self, data_json):
        self.product_json = data_json

    def get_component(self):
        url = ST_Pre_Url + self.product_json["productFolderUrl"]
        code = self.product_json["cells"][0]["value"]
        kiname = "Smartcard Interfaces"

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


        many_attributes = []

        for attributes_value in attributes_values:
            columnId = attributes_value["columnId"]
            attribute_key = ST_Relation[columnId]
            if columnId in ("962", "960"):
                attribute_value = attributes_value["value"].split(",")[0]
            else:
                attribute_value = attributes_value["value"]
            attribute = (attribute_key, attribute_value,)
            many_attributes.append(attribute)

        return many_attributes


if __name__ == "__main__":
    productlist = ProductList()
    data_json = productlist.get_product_list()
    print(data_json)
