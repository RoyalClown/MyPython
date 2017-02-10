"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/12
"""
import re

import requests
from bs4 import BeautifulSoup

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

    def get_code_urls(self, series_url):
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

        product_urls = []
        page_urls = get_pages_urls(series_url)
        if page_urls is None:
            return None
        for page_url in page_urls[:]:
            html_analyse = HtmlAnalyse(page_url)
            bs_contents = html_analyse.get_bs_contents()
            lists = bs_contents.find_all(name='tr', attrs={"class": re.compile(u"(^odd$)|(^even$)")})
            if not lists:
                continue
            for list in lists[1:]:
                try:
                    model = list.td.a
                    code = model.text
                except:
                    break

                # *******去重*******
                orcl_con = OracleConnection()
                cursor = orcl_con.conn.cursor()
                cursor.execute("select cc_id from product$component_crawl where cc_code='{}'".format(code))
                data = cursor.fetchone()
                if data:
                    print("repeat")
                    continue
                cursor.close()
                orcl_con.conn.close()
                # *******结束*******

                href = model.get("href")
                url = Panasonic_Pre_Url + href
                product_urls.append(url)
        return product_urls


class Detail:
    def __init__(self, url):
        self.url = url
        html_analyse = HtmlAnalyse(self.url)
        self.bs_content = html_analyse.get_bs_contents()

    def get_component(self):
        # cc_url
        url = self.url

        # cc_code
        code = self.bs_content.find(name='span', attrs={'id': "model-info-model-number"}).text.replace('.', ' ')[3:]

        # cc_kiname
        kiname = self.bs_content.find(name='span', attrs={'id': "model-info-series-type"}).text.replace('.', ' ')[3:]

        rough_img = self.bs_content.find(name='img', attrs={'typeof': 'foaf:Image'}).get('src')
        # cc_img
        img = Panasonic_Pre_Url + rough_img

        rough_attach = self.bs_content.find(name='a', text=re.compile(r'产品样本')).get('href')
        # cc_attach
        attach = Panasonic_Pre_Url + rough_attach

        component = [url, code, kiname, img, attach]
        return component

    def get_properties(self):
        many_properties = []
        lists = self.bs_content.find(name='table', attrs={'class': 'spec-table'}).tbody.find_all(name='tr')

        for tr_tag in lists:
            key_value = tr_tag.find_all(name='td')
            propertyname = key_value[0].text.strip()
            value = key_value[1].text
            if value == '已应对':
                value = 'YES'
            properties = [propertyname, value]
            many_properties.append(properties)
        return many_properties


if __name__ == "__main__":
    productlist = ProductList()
