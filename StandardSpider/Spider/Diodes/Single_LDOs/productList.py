"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/21
"""
import json
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Diodes.DiodesConstant import Diodes_Product_Pre_Url, Diodes_Relation


class ProductList:
    def __init__(self, url="http://www.diodes.com/catalog/Single_LDOs_50"):
        self.url = url

    def get_product_list(self):
        res = requests.post("http://www.diodes.com/api/catalog/50/products")
        contents = res.content.decode("utf-8")

        data_json = json.loads(contents)
        return data_json["products"], data_json["result"]


class Detail:
    def __init__(self, product_json, result_json):
        self.product_json = product_json
        self.result_json = result_json

    def get_component(self):
        url = Diodes_Product_Pre_Url + self.product_json["url"]
        code = self.product_json["name"]
        kiname = "Single_LDOs"

        img = ""
        try:
            attach = Diodes_Product_Pre_Url + self.result_json["values"]["1"][0]
        except:
            attach = ""

        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        try:
            many_attributes = [("Package Outlines", self.product_json["packages"][0]["name"])]
        except:
            many_attributes = [("Package Outlines", "")]
        for k, v in self.result_json["values"].items():
            if k == "2":
                attribute = (Diodes_Relation[k], Diodes_Product_Pre_Url + v[0],)
            elif k != "1":
                attribute = (Diodes_Relation[k], v[0],)
            else:
                continue
            many_attributes.append(attribute)

        return many_attributes
