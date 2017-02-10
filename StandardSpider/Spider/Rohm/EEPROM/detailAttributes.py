"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/14
"""
import re

from bs4 import BeautifulSoup

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class DetailAttributes:
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
    detailattributes = DetailAttributes(
        ("a", "http://www.rohm.com.cn/web/china/products/-/product/BR24A01AF-WLB(H2)", ""))
    detailattributes.get_base_attributes()
    # detailattributes.get_component()
