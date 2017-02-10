"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/14
"""
from bs4 import BeautifulSoup

from Spider.Rohm.RohmConstant import Rohm_Pre_Url


class ProductList:
    def __init__(self):
        pass

    def get_urls_pdfs(self):
        with open("I:\PythonPrj\StandardSpider\Spider\Rohm\EEPROM\htmlcode.html", "r", encoding="utf-8") as f:
            content = f.read()
        bs_content = BeautifulSoup(content, "html.parser")
        all = bs_content.find_all(name="td", attrs={"align": "left", "class": "part-name PartNumber"})
        pdfs_urls = []
        for one in all:
            tag_url_pdf = one.find_all(name="div")
            url_code = tag_url_pdf[0].a
            code = url_code.text
            url = Rohm_Pre_Url + url_code.get("href")
            pdf = tag_url_pdf[1].a.get("link")
            pdf_url = (code, url, pdf,)
            pdfs_urls.append(pdf_url)
        return pdfs_urls


if __name__ == "__main__":
    productlist = ProductList()
    productlist.get_urls_pdfs()
