"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/5
"""
import re

import requests
from bs4 import BeautifulSoup

from Lib.DBConnection.OracleConnection import OracleConnection
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.PanasonicDevice.PanasonicDeviceConstant import Pre_Panasonic_Device_Url


class ProductList:
    def __init__(self):
        self.series_urls = ["http://device.panasonic.cn/ac/c/control/sensor/human/wl/number/index.jsp?c=search",
                            "http://device.panasonic.cn/ac/c/control/sensor/human/vz/number/index.jsp?c=search",
                            "http://device.panasonic.cn/ac/c/control/sensor/human/napion/number/index.jsp?c=search"]

    def get_all_content(self):
        many_contents = []
        for series_url in self.series_urls:
            if series_url == "http://device.panasonic.cn/ac/c/control/sensor/human/wl/number/index.jsp?c=search":
                session = requests.session()
                session.headers.update({
                    'Connection': 'keep-alive',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'zh-CN,zh;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Cache-Control': 'max-age=0',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Host': 'device.panasonic.cn',
                    'Origin': 'http://device.panasonic.cn',
                    'Referer': 'http://device.panasonic.cn/ac/c/control/sensor/human/wl/number/index.jsp?c=search',
                    'Upgrade-Insecure-Requests': '1'
                })
                form = {'pagecnt': 1, 'maxrows': 20, 'topage': 2, 'VAL_3_3286': '', 'VAL_3_3433': '', 'VAL_3_3287': '',
                        'VAL_3_3436': '', 'part_no': ''}
                content0 = session.get(series_url).text
                bs_contents0 = BeautifulSoup(content0, "html.parser")
                many_contents.append(bs_contents0)
                content1 = session.post(
                    "http://device.panasonic.cn/ac/c/control/sensor/human/wl/number/index.jsp?c=move", data=form).text
                bs_contents1 = BeautifulSoup(content1, "html.parser")
                many_contents.append(bs_contents1)
            else:
                html_analyse = HtmlAnalyse(series_url)
                bs_contents = html_analyse.get_bs_contents()
                many_contents.append(bs_contents)
        return many_contents

    def get_product_list(self):
        series_contents = self.get_all_content()
        urls = []
        codes = []
        for series_content in series_contents:
            rough_urls_codes = series_content.find_all(name="a", attrs={
                "href": re.compile(r'/ac/c/search_num/index\.jsp')})
            for rough_url_code in rough_urls_codes:
                code = rough_url_code.text

                orcl_con = OracleConnection()
                cursor = orcl_con.conn.cursor()
                cursor.execute("select cc_id from product$component_crawl where cc_code='{}'".format(code))
                data = cursor.fetchone()
                if data:
                    print("repeat")
                    continue
                cursor.close()
                orcl_con.conn.close()

                rough_url = rough_url_code.get("href")
                re_url = re.match(r'(/ac/c/search_num/index\.jsp).*?(\?c=detail&part_no=.*$)', rough_url)
                url = Pre_Panasonic_Device_Url + re_url.group(1) + re_url.group(2)
                codes.append(code)
                urls.append(url)
        return urls, codes


class Detail:
    def __init__(self, url, code):
        self.url = url
        self.code = code
        html_analyse = HtmlAnalyse(self.url)
        self.bs_content = html_analyse.get_bs_contents()

    def get_component(self):
        url = self.url
        code = self.code.strip()

        kiname = "焦电型红外线传感器 PaPIRs"

        rough_pdf = self.bs_content.find(name="a", text="样本", attrs={
            "href": re.compile(r"/ac/c/dl/catalog/index\.jsp\?series_cd=")})
        rough_pdf_url = Pre_Panasonic_Device_Url + rough_pdf.get("href")

        rough_img = self.bs_content.find(name="img", attrs={"class": "max_img01"})

        img = Pre_Panasonic_Device_Url + rough_img.get("src")

        def get_pdf(url):
            html_analyse = HtmlAnalyse(url)
            bs_content = html_analyse.get_bs_contents()
            pdf = bs_content.find(name="a",
                                  attrs={"href": re.compile(r'/ac/c_download/.*?\.pdf')})
            if pdf:
                pdf_url = pdf.get("href") + "&via=ok"
            else:
                pdf_url = ''
            return pdf_url

        attach = Pre_Panasonic_Device_Url + get_pdf(rough_pdf_url)
        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        rohs_flag = self.bs_content.find(name="img", attrs={"src": "/ac/c/common/images/pn_module/namaei.gif"})
        if rohs_flag:
            many_attributes = [("RoHS指令", "无铅"), ]
        else:
            many_attributes = []
        attributes = self.bs_content.find_all(name="td", attrs={"class": re.compile(r"spec_table_td_0")})
        for tag_name, tag_value in zip(range(4, len(attributes), 2), range(5, len(attributes), 2)):
            name = attributes[tag_name].text
            value = attributes[tag_value].text
            attribute = (name, value,)
            many_attributes.append(attribute)
        return many_attributes


if __name__ == "__main__":
    productlist = ProductList()
    productlist.get_product_list()
