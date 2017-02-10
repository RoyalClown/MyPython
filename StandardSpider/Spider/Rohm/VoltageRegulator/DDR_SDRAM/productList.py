"""
    @description:   来源:kionix
                    商城品牌:Kionix
                    目标类目:加速度计
                    商城类目:加速计/加速度传感器
                    来源网址:http://zh-cn.kionix.com/parametric/Accelerometers
    @author:        RoyalClown
    @date:          2016/11/17
"""
import re

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Kionix.KionixConstant import Kionix_Pdf_Pre_Url, Kionix_Product_Pre_Url

from bs4 import BeautifulSoup

from Spider.Rohm.RohmConstant import Rohm_Pre_Url


class ProductList:
    def __init__(self):
        pass

    def get_urls_pdfs(self):
        with open("I:\PythonPrj\StandardSpider\Spider\Rohm\VoltageRegulator\WatchDog\htmlcode.html", "r",
                  encoding="utf-8") as f:
            content = f.read()
        bs_content = BeautifulSoup(content, "html.parser")
        all = bs_content.find_all(name="td", attrs={"align": "left", "class": "part-name PartNumber"})
        pdfs_urls = []
        for one in all:
            tag_url_pdf = one.find_all(name="div")
            url_code = tag_url_pdf[0].a
            code = url_code.text
            url = Rohm_Pre_Url + url_code.get("href")
            try:
                pdf = tag_url_pdf[1].a.get("link")
            except:
                pdf = ""
            pdf_url = (code, url, pdf,)
            pdfs_urls.append(pdf_url)
        return pdfs_urls


class Detail:
    def __init__(self, url_pdf):
        self.code = url_pdf[0]
        self.url = url_pdf[1]
        self.pdf = url_pdf[2]

        html_analyse = HtmlAnalyse(self.url)
        self.content = html_analyse.get_contents()

    def get_component(self):
        url = self.url
        code = self.code
        kiname = "串行EEPROM"
        attach = self.pdf
        rough_img = re.search(r'productThumnailImageLogo="(http://rohmfs\.rohm\.com.*?\.jpg)"', self.content)
        try:
            img = rough_img.group(1)
        except:
            img = ""
        component = [url, code, kiname, img, attach]
        return component

    def get_base_attributes(self):
        bs_content = BeautifulSoup(self.content, "html.parser")
        base_names_values = bs_content.find(name="table", attrs={"class": "datatable customdesign"}).find_all("tr")
        base_names = base_names_values[0].find_all("th")[1:]
        base_values = base_names_values[1].find_all("td")[1:]

        many_attributes = []
        for base_name, base_value in zip(base_names, base_values):
            attribute_name = base_name.div.text
            try:
                attribute_value = base_value.a.text.strip()
            except:
                attribute_value = base_value.text
            attribute = (attribute_name, attribute_value,)
            many_attributes.append(attribute)

        other_attributes = bs_content.find_all(name="td", attrs={"class": "list"})
        for tag_name, tag_value in zip(range(0, len(other_attributes), 2), range(1, len(other_attributes), 2)):
            name = other_attributes[tag_name].text
            value = other_attributes[tag_value].text
            other_attribute = (name, value,)
            many_attributes.append(other_attribute)
        return many_attributes


if __name__ == "__main__":
    # productlist = ProductList()
    # productlist.get_urls_pdfs()

    detailattributes = Detail(
        ("a", "http://www.rohm.com.cn/web/china/products/-/product/BR24A01AF-WLB(H2)", ""))
    detailattributes.get_base_attributes()
    # detailattributes.get_component()
