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
from Spider.Vishay.VishayConstant import Vishay_Pre_Url


class ProductList:
    def __init__(self, url="http://www.vishay.com/diodes/rectifiers/bridge/reverse-voltage-gt-50-v-lteq-60-v/"):
        self.url = url

    def get_product_list(self):
        html_analyse = HtmlAnalyse(self.url)
        bs_content = html_analyse.get_bs_contents()
        rough_products_list = bs_content.find_all(name="tr", attrs={"class": re.compile(r'^doc-')})
        return rough_products_list


class Detail:
    def __init__(self, rough_product):
        self.rough_product = rough_product

    def get_component(self):
        url_code = self.rough_product.find(name="div", attrs={"class": "serLnk"}).a
        url = Vishay_Pre_Url + url_code.get("href")
        code = url_code.text
        kiname = "REVERSE VOLTAGE 600 TO 1000 V"

        img = Vishay_Pre_Url + self.rough_product.find(name="img", attrs={
            "src": re.compile(r'/images/product-images.*?\.jpg$')}).get("src").replace("small", "large")

        attach_url = Vishay_Pre_Url + self.rough_product.find(name="div", attrs={"class": "pdfLnk"}).a.get("href")
        def get_attach(attach_url):
            html_analyse = HtmlAnalyse(attach_url)
            bs_content = html_analyse.get_bs_contents()
            attach = Vishay_Pre_Url + bs_content.find(name="meta", attrs={"content": re.compile(r'^/docs/.*?\.pdf$')}).get("content")
            return attach
        attach = get_attach(attach_url)
        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        rough_attributes = self.rough_product.find_all(name="td")
        relation_list = ("Package", "IF(AV) (A)", "IFSM (A)", "Rev. Voltage (V)", "VF at IF (V at A)", "Tj max. (°C)",
                         "Diode Variations")
        many_attributes = []
        for rough_attribute, relation_name in zip(rough_attributes[2:], relation_list):
            attribute_name = relation_name
            attribute_value = rough_attribute.text
            attribute = (attribute_name, attribute_value)
            many_attributes.append(attribute)

        return many_attributes


if __name__ == "__main__":
    productlist = ProductList()
    data_json = productlist.get_product_list()
    print(data_json)
