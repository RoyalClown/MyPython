"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/15
"""
import re

import requests
from bs4 import BeautifulSoup

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.PanasonicDevice.PanasonicDeviceConstant import Pre_Panasonic_Device_Url


class ProductList:
    def __init__(self, url="http://device.panasonic.cn/ac/c/control/list_search_spec/photomos/index.jsp"):
        self.url = url
        self.products_count = 1

    def get_pages_contents(self):
        pages_count = int(self.products_count / 20 + 1)
        all_pages_content = []
        for page_num in range(1, pages_count + 1):
            form_data = {'pagecnt': 2, 'maxrows': 20, 'topage': pages_count, 'fq_spec': '', 'fq_value': '',
                         'spec_3_1361_s_fq': '', 'spec_3_1366_s_fq': '', 'spec_3_1369_s_fq': '', 'spec_3_1362_s_fq': '',
                         'spec_3_1372_s_fq': '', 'spec_3_1375_s_fq': '', 'spec_3_1363_s_fq': '', 'spec_3_1399_s_fq': '',
                         'spec_3_1380_s_fq': '', 'spec_3_1391_s_fq': '', 'rows': 20}
            res = requests.post(self.url, data=form_data)
            contents = res.content.decode("utf-8")
            bs_contents = BeautifulSoup(contents, "html.parser")
            all_pages_content.append(bs_contents)
        return all_pages_content

    def get_product_list(self):
        all_pages_contents = self.get_pages_contents()
        product_urls = []
        product_codes = []
        for page_content in all_pages_contents:
            rough_product_urls = page_content.find_all(name="a", attrs={
                "href": re.compile(r'/ac/c/search_num/index\.jsp\?c=detail&part_no=')})
            for rough_product_url in rough_product_urls:
                url = Pre_Panasonic_Device_Url + rough_product_url.get("href")
                code = rough_product_url.text

                product_urls.append(url)
                product_codes.append(code)

        return product_urls, product_codes


class Detail:
    def __init__(self, url, code):
        self.url = url
        self.code = code
        html_analyse = HtmlAnalyse(self.url)
        self.bs_content = html_analyse.get_bs_contents()

    def get_component(self):
        url = self.url
        code = self.code.strip()
        kiname = "PhotoMOS(MOSFET输出光电耦合器)"

        rough_pdf = self.bs_content.find(name="a", text="样本", attrs={"href": re.compile(r"/ac/c/dl/catalog/index\.jsp\?series_cd=1939&part_no=")})
        rough_pdf_url = Pre_Panasonic_Device_Url + rough_pdf.get("href")

        rough_img = self.bs_content.find(name="img", attrs={"class": "max_img01"})

        img = Pre_Panasonic_Device_Url + rough_img.get("src")

        def get_pdf(url):
            html_analyse = HtmlAnalyse(url)
            bs_content = html_analyse.get_bs_contents()
            pdf = bs_content.find(name="a",
                                  attrs={"href": re.compile(r'/ac/c_download/control/relay/photomos/catalog/semi_cn_')})
            pdf_url = pdf.get("href") + "&via=ok"
            return pdf_url

        attach = Pre_Panasonic_Device_Url + get_pdf(rough_pdf_url)
        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        many_attributes = []
        attributes = self.bs_content.find_all(name="td", attrs={"class": re.compile(r"spec_table_td_0")})
        for tag_name, tag_value in zip(range(4, len(attributes)-4, 2), range(5, len(attributes)-3, 2)):
            name = attributes[tag_name].text
            value = attributes[tag_value].text
            attribute = (name, value,)
            many_attributes.append(attribute)
        return many_attributes

if __name__ == "__main__":
    productlist = ProductList()
    productlist.get_product_list()
