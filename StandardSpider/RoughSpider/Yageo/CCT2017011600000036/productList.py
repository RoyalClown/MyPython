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
        data1 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_CFilm", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_CFilm", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data2 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_Fwirewound", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_Fwirewound", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data3 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_LowOhmWire", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_LowOhmWire", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data4 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_MetalFilm", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_MetalFilm", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data5 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_MetalGlazedFilm", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_MetalGlazedFilm", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data6 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_OFilm", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_OFilm", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data7 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_PulseLoad", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_PulseLoad", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data8 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_Wirewound", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_Wirewound", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data9 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_ZeroOhm", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_ZeroOhm", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data10 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_Cement", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_Cement", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}
        data11 = {"Category_Radio": "LeadedR", "Feature_Radio": "LeadedR_AlumiHouse", "CATEGORY": "LeadedR",
                "FEATURE": "LeadedR_AlumiHouse", "INDUCTANCE": "", "TOLERANCE": "", "IMPEDANCE": "", "SIZE": "",
                "POWER": "",
                "RESISTANCE": "", "TCR": "", "CAPACITANCE": "", "TC": "", "VOLTAGE": "", "FREQUENCY": "",
                "INSERTIONLOSS": "",
                "LIFETIME": "", "ANTENNA": "",
                "ISSEARCH": "OK"}

        datas = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11]
        all_product_tags = []
        for data in datas:
            contents = html_analyse.post_contents(data=data).encode().decode()
            bs_contents = BeautifulSoup(contents, "html.parser")
            product_tags = bs_contents.find_all(name="tr")[1:]
            all_product_tags += product_tags
        return all_product_tags


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
    with open("../CCT2017011600000036.csv", "w", encoding="utf-8") as f:
        f.write(
            "pdf, Part No.,Series Name,Rated Power,Tolerance,T.C.R,Resistance Value\n")
        for product_tag in product_tags:
            detail = Detail(product_tag)
            component = detail.get_component()
            print(component)
            line = (",".join(component)) + "\n"
            f.write(line.encode().decode())
