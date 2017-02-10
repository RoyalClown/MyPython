"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/6
"""
import json
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.TI.TIConstant import TI_Relation


class ProductList:
    def __init__(self,
                 url="http://www.ti.com.cn/lsds/ti_zh/power-management/ldo-controller-external-fet-products.page"):
        self.url = url

    def get_product_list(self):
        html_analyse = HtmlAnalyse("http://www.ti.com.cn/wsapi/paramdata/family/465/results?lang=cn&output=json")
        contents = html_analyse.get_contents()

        datas_jsons = json.loads(contents)
        return datas_jsons["ParametricResults"]


class Detail:
    def __init__(self, product_json):
        self.product_json = product_json

    def get_component(self):
        url = "http://www.ti.com.cn/lsds/ti_zh/power-management/single-channel-ldo-products.page?"
        code = self.product_json["o1"]
        kiname = "多通道 LDO 产品"

        img = "http://www.ti.com/graphics/folders/partimages/" + code + ".jpg"
        attach = "http://www.ti.com.cn/cn/lit/ds/symlink/" + code.lower() + ".pdf"
        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        many_attributes = []
        for cid, value in self.product_json.items():
            attribute_key = TI_Relation[cid]
            if cid in ("p1130", "p1811"):
                continue
            else:
                attribute_value = value
            attribute = (attribute_key, attribute_value,)
            many_attributes.append(attribute)

        return many_attributes


if __name__ == "__main__":
    productlist = ProductList()
    data_json = productlist.get_product_list()
    print(data_json)
