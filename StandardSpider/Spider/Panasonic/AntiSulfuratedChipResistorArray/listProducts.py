"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/14
"""
import re

from Lib.DBConnection.OracleConnection import OracleConnection
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Panasonic.PanasonicConstant import Third_Suffix_Url, Panasonic_Pre_Url


class ProductList:
    def __init__(self):
        pass

    def get_series_urls(self, list_url):

        def get_pages_urls(url):
            html_analyse = HtmlAnalyse(url)
            bs_contents = html_analyse.get_bs_contents()
            page_urls = []
            page = len(bs_contents.find_all(name="li", attrs={"class": "pager-item"})) + 1
            for i in range(page):
                page_url = url.split('#')[0] + "?page=" + str(i) + Third_Suffix_Url
                page_urls.append(page_url)
            return page_urls

        series_urls = []
        page_urls = get_pages_urls(list_url)
        if page_urls is None:
            return None
        for page_url in page_urls:
            html_analyse = HtmlAnalyse(page_url)
            bs_contents = html_analyse.get_bs_contents()
            tags = bs_contents.find_all(name='tr', attrs={"class": re.compile(u"ecatalog-series-table")})
            for tag in tags:
                try:
                    href = tag.find_all(name="td")[0].a.get("href")
                    m_url = Panasonic_Pre_Url + href + '&limit=100'
                    series_urls.append(m_url)
                except Exception as e:
                    href = tag.find_all(name="td")[1].a.get("href")
                    m_url = Panasonic_Pre_Url + href + '&limit=100'
                    series_urls.append(m_url)

        return series_urls

    def get_products_list(self, series_url):
        def get_pages_urls(url):
            html_analyse = HtmlAnalyse(url, is_proxy=True)
            bs_content = html_analyse.get_bs_contents()
            page_tag = bs_content.find(name="a", attrs={"title": "到最后一页"}, text="末页 »")
            try:
                rough_page = page_tag.get("href")
                page = re.match(r"/ea/products/.*?page=(\d+)&reset=1", rough_page).group(1)
            except:
                page = 0
            page_urls = []
            for i in range(int(page) + 1):
                page_url = url + "&page=" + str(i)
                page_urls.append(page_url)
            return page_urls

        product_lists = []
        page_urls = get_pages_urls(series_url)
        if page_urls is None:
            return None
        for page_url in page_urls[:]:
            html_analyse = HtmlAnalyse(page_url)
            bs_contents = html_analyse.get_bs_contents()
            product_list = bs_contents.find_all(name='tr', attrs={"class": re.compile(u"(^odd$)|(^even$)")})[1:]
            if not product_list:
                continue
            product_lists += product_list
        return product_lists


class Detail:
    def __init__(self, product_list):
        self.product_list = product_list

    def get_component(self, kiname, img, attach):
        # cc_url
        url = Panasonic_Pre_Url + self.product_list.td.a.get('href')

        # cc_code
        code = self.product_list.td.a.text

        component = [url, code, kiname, img, attach]
        return component

    def get_properties(self):
        relation = {3: "SMD", 4: "片式尺寸(长 x 宽)", 5: "电阻值 (Ohm)", 6: "电阻值容差", 7: "包装形状", 11: "电阻温度系数", 8: "端子间距",
                    9: "电路结构", 10: "元件数量 (个)", 12: "端子数量"}
        td_tags = self.product_list.find_all(name="td")
        many_properties = []
        for i, key in relation.items():
            propertyname = key
            value = td_tags[i].text
            properties = [propertyname, value]
            many_properties.append(properties)
        return many_properties


if __name__ == "__main__":
    productlist = ProductList()
