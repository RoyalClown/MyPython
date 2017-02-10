"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/15
"""
import re

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Azurewave.AzurewaveConstant import Azurewave_Pre_Url


class DetailAttributes:
    def __init__(self, url="http://www.azurewave.com/product_a001_1.asp"):
        self.url = url
        html_analyse = HtmlAnalyse(self.url)
        self.bs_content = html_analyse.get_bs_contents()

    def get_product_list(self):

        strong_tags = self.bs_content.find_all(name="strong", text=re.compile("^AW-"))
        products_lists = []
        for strong_tag in strong_tags:
            product_list = strong_tag.parent
            products_lists.append(product_list.contents)
        img_list = self.bs_content.find_all(name="img", attrs={"src": re.compile(r"\.png$")})

        return products_lists, img_list

    def get_components(self, product_tag, img_tag):
        url = self.url
        kiname = "Wifi 模块"
        attach = ""

        code = product_tag[0].text
        img = Azurewave_Pre_Url + img_tag.get("src")
        component = [url, code, kiname, img, attach,]
        return component

    def get_attributes(self, product_tag):
        attrs = product_tag[1].text.split("\r\n")
        many_attributes = []
        for attr in attrs[1:]:
            if ":" in attr:
                attr_key_value = attr.strip().split(":")
                attribute = [attr_key_value[0], attr_key_value[1]]
            else:
                attr_key_value = attr.strip().split(" ")
                attribute = [attr_key_value[1], attr_key_value[0]]
            many_attributes.append(attribute)
        return many_attributes


if __name__ == "__main__":
    detailattributes = DetailAttributes("http://www.azurewave.com/product_a001_1_SC.asp")
    detailattributes.get_product_list()