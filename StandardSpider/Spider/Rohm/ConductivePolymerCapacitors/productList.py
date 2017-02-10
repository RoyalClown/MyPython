"""
    @description:
    @author:        RoyalClown
    @date:          2016/12/12
"""
import re

from Lib.DBConnection.OracleConnection import OracleConnection
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse

from bs4 import BeautifulSoup

from Spider.Rohm.RohmConstant import Rohm_Pre_Url


class ProductList:
    def __init__(self):
        pass

    def get_urls_pdfs(self):
        with open("I:\PythonPrj\StandardSpider\Spider\Rohm\ConductivePolymerCapacitors\htmlcode.html", "r",
                  encoding="utf-8") as f:
            content = f.read()
        bs_content = BeautifulSoup(content, "html.parser")
        all = bs_content.find_all(name="td", attrs={"align": "left", "class": "part-name PartNumber"})
        pdfs_urls = []
        for one in all:
            tag_url_pdf = one.find_all(name="div")
            url_code = tag_url_pdf[0].a
            code = url_code.text

            orcl_con = OracleConnection()
            cursor = orcl_con.conn.cursor()
            cursor.execute("select cc_id from product$component_crawl where cc_code='{}'".format(code))
            data = cursor.fetchone()
            if data:
                print("repeat")
                continue
            cursor.close()
            orcl_con.conn.close()

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

    def   get_component(self):
        url = self.url
        code = self.code
        kiname = "贴片钽电容器"
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
    productlist = ProductList()
    productlist.get_urls_pdfs()
