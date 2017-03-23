import re

import requests
import sys
from bs4 import BeautifulSoup

from Components.DBSAVE.oracleSave import OracleSave
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class Category:
    def __init__(self):
        self.proxy_pool = ProxyPool()

    def get_categories(self):
        main_url = "http://www.chip1stop.com/web/CHN/zh/dispClassSearchTop.do"
        self.proxy_ip = self.proxy_pool.get()
        while True:
            try:
                html_analsye = HtmlAnalyse(main_url, proxy=self.proxy_ip)
                bs_content = html_analsye.get_bs_contents()
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()

        dl_tags = bs_content.find_all(name="dl", attrs={"class": "categoryListDl clearfix"})

        second_categories = []
        for dl_tag in dl_tags:
            first_directory_name = dl_tag.dt.text
            second_directory_tags = dl_tag.find_all(name="dd")
            for second_directory_tag in second_directory_tags:
                rough_second_directory_name = second_directory_tag.text
                second_directory_name = re.match(r"(.*?)\[", rough_second_directory_name).group(1).strip()
                second_directory_url = "http://www.chip1stop.com/web/CHN/zh" + second_directory_tag.span.a.get("href")[
                                                                               1:]
                second_directory = (first_directory_name, second_directory_name, second_directory_url)
                second_categories.append(second_directory)
        return second_categories

    def get_product_list(self):
        categories = self.get_categories()
        form_data = {
            "nextSearchIndex": "0",
            "dispPageNo": "1",
            "dispNum": "100",
            "type": "page"
        }
        request_headers = {
            "Accept": "text/html, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://www.chip1stop.com",
            "Host": "www.chip1stop.com",
            "Proxy-Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.14 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        request_cookie = {
            "CK_005": "jS1czThT76C51HOUQ42UtQ06TsvRnzI105VoKAixt4s=",
            "CK_002": "aYWM1+FztffTlWgoCLG3iw==",
            "CK_001": "v1gP31jjkR0=",
            "CK_007": "cPDwiM71wuQ=",
            "CK_006": "kQp2UYR7V1g=",
            "CK_008": "i0dI70Swgcs=",
            "WMONID": "VvpmCoTZsss",
            "_gat": "1",
            "_ga": "GA1.2.1422864444.1488415703",
            "JSESSIONIDVERSION": "2f633173:8",
            "JSESSIONID": "b7d640d0a05a7885ab3cab0168cf.ap2",
            "JREPLICA": "c1-instance6",
            "id": "27e37541744912b7||t=1486458155|et=730|cs=002213fd4869c45d604be72033",
            "Referer": "https://www.chip1stop.com/web/CHN/zh/login.do"
        }
        complete_form_data = {
            "nextSearchIndex": "0",
            "dispPageNo": "1",
            "dispNum": "25",
            "rental": "false",
            "partSameFlg": "false",
            "subWinSearchFlg": "false",
            "used": "false",
            "newProductFlg": "false",
            "newProudctHandlingFlg": "false",
            "newSameDayShippedFlg": "false",
            "eventId": "0001",
            "searchType": "2",
            "dispAllFlg": "true",
        }

        def thread_go(page_no):
            print("Page:", page_no)

            page_parts = range(0, 25, 5)
            for page_part in page_parts:
                print("Part:", page_part)
                # def thread_go(page_part):
                complete_form_data['nextSearchIndex'] = page_part
                complete_form_data['dispPageNo'] = page_no
                complete_form_data['type'] = "page"
                detail_url = second_category_url + "&dispPageNo=%d" % page_no

                while True:
                    try:
                        my_session.cookies.update(request_cookie)
                        res = my_session.post(detail_url, data=complete_form_data, proxies=self.proxy_ip,
                                              timeout=20)
                        print(res.status_code)
                        if res.status_code == 200:
                            content = res.content.decode()
                            bs_content = BeautifulSoup(content, "lxml")
                            tr_tags = bs_content.find_all(name="tr")[1:]
                            if tr_tags:
                                break
                        else:
                            self.proxy_pool.remove(self.proxy_ip)
                            self.proxy_ip = self.proxy_pool.get()
                    except Exception as e:
                        print(sys._getframe().f_code.co_name, e)
                        self.proxy_pool.remove(self.proxy_ip)
                        self.proxy_ip = self.proxy_pool.get()
                tr_tags = bs_content.find_all(name="tr")[1:]
                if not tr_tags:
                    continue
                # 数据库连接
                orcl_conn = OracleSave(1000001)

                for tr_tag in tr_tags:
                    try:
                        code = tr_tag.td.find(name="p", attrs={"class": "text14pt2 bold"}).text.strip()
                    except Exception as e:
                        print(e)
                        continue

                    chip1stop_code = tr_tag.td.find(name="p", attrs={"class": "text10"}).text.strip()
                    print(chip1stop_code)
                    maker = tr_tag.td.find(name="p", attrs={"class": "text10 wordBreak"}).text.strip()
                    pdf_url = tr_tag.find(name="a", attrs={"href": re.compile(r"http://download\.siliconexpert\.com/pdfs")})
                    if pdf_url:
                        pdf_url = pdf_url.get("href")

                    component = (code, maker, first_category_name, second_category_name, second_category_url, pdf_url, None)
                    orcl_conn.component_insert(component)

                    property_tags = tr_tag.find_all(name="td")[6:-1]
                    for property_name, property_tag in zip(property_names, property_tags):
                        if property_name == '购买/询价':
                            continue
                        property_value = property_tag.text
                        if property_value:
                            property_value = property_value.strip()
                        single_property = (property_name, property_value)
                        orcl_conn.properties_insert(single_property)

                orcl_conn.commit()
                orcl_conn.conn.close()

        # def thread_go(page_no):

        for category in categories:
            first_category_name, second_category_name, second_category_url = category

            while True:
                try:
                    my_session = requests.session()
                    my_session.headers.update(request_headers)
                    self.proxy_ip = self.proxy_pool.get()
                    res = my_session.post(second_category_url, data=form_data, proxies=self.proxy_ip, timeout=10)
                    print(res.status_code)
                    if res.status_code == 200:
                        break
                    self.proxy_pool.remove(self.proxy_ip)
                    self.proxy_ip = self.proxy_pool.get()
                except Exception as e:
                    print(sys._getframe().f_code.co_name, e)
                    self.proxy_pool.remove(self.proxy_ip)
            content = res.content.decode()
            bs_content = BeautifulSoup(content, "lxml")
            products_count = bs_content.find(name="span", attrs={"class": "bold_red"}).text.replace(",", "").replace(
                "件", "")
            table_headers_tag = bs_content.find(name="tr", attrs={"class": "parent"})
            property_name_tags = table_headers_tag.find_all(name="td")
            # 器件参数名称
            property_names = []
            for property_name_tag in property_name_tags[6:-1]:
                property_name = property_name_tag.text.strip()
                property_names.append(property_name)
            # 总页数
            pages_count = int(int(products_count) / 25) + 1

            if pages_count > 400:
                pages_count = 400

            # for page_no in range(1, pages_count + 1):

            # ---------------------------我是分割线----------------------------

            # threading_pool = ThreadingPool(10)
            # threading_pool.multi_process(thread_go, list(range(1, pages_count + 1)))

            for i in range(1, pages_count + 1):
                thread_go(i)


if __name__ == "__main__":
    category = Category()
    category.get_product_list()
