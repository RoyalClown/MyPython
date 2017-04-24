"""
    @description:   
    @author:        RoyalClown
    @date:          2017/4/6
"""
import csv
import re
import sys

import requests
from bs4 import BeautifulSoup

from Components.DBSAVE.oracleSave import OracleSave
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class MouserGo:
    def __init__(self):
        self.proxy_pool = ProxyPool()
        self.proxy_ip = self.proxy_pool.get()
        self.mouser_host_url = "http://www.mouser.cn"
        self.my_session = requests.session()

    def get_all_category(self):
        while True:
            try:
                self.my_session.proxies.update(self.proxy_ip)
                my_headers = {'Connection': 'Keep-Alive',
                              'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                              'Accept-Encoding': 'gzip, deflate, sdch',
                              "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
                              "Host": "www.mouser.cn", "Upgrade-Insecure-Requests": "1",
                              "Referer": "http://www.mouser.cn/Electronic-Components/", }
                self.my_session.headers.update(my_headers)
                res = self.my_session.get("http://www.mouser.cn/Electronic-Components/")
                if res.status_code != 200:
                    print(res.status_code)
                    self.proxy_pool.remove(self.proxy_ip)
                    self.proxy_ip = self.proxy_pool.get()
                    continue
                bs_content = BeautifulSoup(res.content, "lxml")
                category_url_tags = bs_content.find_all(name="a", attrs={"class": "SearchResultsSubLevelCategory"})
                if not category_url_tags:
                    print(sys._getframe().f_code.co_name, "category_url_tag is None")
                    continue
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
        multi_category_structures = []
        for category_url_tag in category_url_tags:
            url = self.mouser_host_url + category_url_tag.get("href")[2:]
            single_category_structures = self.get_detail_category(url)
            multi_category_structures += single_category_structures
        return multi_category_structures

    def get_detail_category(self, url):
        while True:
            try:
                detail_headers = {'Connection': 'Keep-Alive',
                                  'Accept-Language': 'zh-CN,zh;q=0.8',
                                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                  'Accept-Encoding': 'gzip, deflate, sdch',
                                  "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36',
                                  "Host": "www.mouser.cn", "Upgrade-Insecure-Requests": "1",
                                  "Referer": "http://www.mouser.cn/Electronic-Components/", }
                self.my_session.proxies.update(self.proxy_ip)
                self.my_session.headers.update(detail_headers)
                res = self.my_session.get(url, timeout=20)
                if res.status_code != 200:
                    print(res.status_code)
                    self.proxy_pool.remove(self.proxy_ip)
                    self.proxy_ip = self.proxy_pool.get()
                    continue
                bs_content = BeautifulSoup(res.content, "lxml")

                first_category_tag = bs_content.find(name="a",
                                                     id="ctl00_ContentMain_bc_rptrBreadcrumbs_ctl01_lnkBreadcrumb")
                if not first_category_tag:
                    self.proxy_pool.remove(self.proxy_ip)
                    print("None, go on")
                    self.proxy_ip = self.proxy_pool.get()
                    continue
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()

        first_category_name = first_category_tag.text
        second_category_tag = bs_content.find(name="a", id="ctl00_ContentMain_bc_rptrBreadcrumbs_ctl02_lnkBreadcrumb")
        second_category_name = second_category_tag.text
        third_category_tag = bs_content.find(name="a", id="ctl00_ContentMain_bc_rptrBreadcrumbs_ctl03_lnkBreadcrumb")
        if third_category_tag:
            third_category_name = third_category_tag.text
        else:
            third_category_name = second_category_name

        detail_category_tags = bs_content.find_all(name="div", attrs={"class": "div-cat-title"})
        category_structures = []
        if detail_category_tags:
            pre_category_url = re.match(r"(.+)/_/.+/$", url).group(1)
            for detail_category_tag in detail_category_tags:
                forth_category_tag = detail_category_tag.a
                forth_category_name = forth_category_tag.text
                forth_category_url = pre_category_url + forth_category_tag.get("href")[5:]
                component_count = detail_category_tag.span.span.text.replace(",", "")
                category_structure = (
                    first_category_name, second_category_name, third_category_name, forth_category_name,
                    forth_category_url,
                    component_count)
                category_structures.append(category_structure)

        else:
            forth_category_name = third_category_name
            forth_category_url = url
            component_count_tag = bs_content.find(name="span", id="ctl00_ContentMain_lblProductCount")
            component_count = component_count_tag.text.replace("(", "").replace(")", "").replace(",", "")

            category_structure = (
                first_category_name, second_category_name, third_category_name, forth_category_name, forth_category_url,
                component_count)
            category_structures.append(category_structure)
        print(category_structures)
        return category_structures

    def category_to_csv(self, category_structure):
        with open("..\\Mouser.csv", "w", encoding="utf-8") as f:
            for category_structure in category_structure:
                modify_category_structure = []
                for category_name in category_structure:
                    modify_category_name = category_name.replace(",", "，")
                    modify_category_structure.append(modify_category_name)
                line = (",".join(modify_category_structure)) + "\n"
                f.write(line.encode().decode())

    def read_from_csv(self):
        csv_categories = []
        with open("..\\Mouser.csv", "r", encoding="utf-8") as f:
            read = csv.reader(f)
            for line in read:
                print(line)
                csv_categories.append(line)
        return csv_categories



    def thread_go(self, category_tree):
        first_category_name = category_tree[0].replace("\ufeff", "")
        second_category_name = str(category_tree[1:-2])
        url, component_count = category_tree[-2:]
        if component_count == 1:
            return
        my_headers = {'Connection': 'Keep-Alive',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Accept-Encoding': 'gzip, deflate, sdch',
                      "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
                      "Host": "www.mouser.cn", "Upgrade-Insecure-Requests": "1", }
        for page_num in range(0, int(component_count), 25):
            page_url = url + "?No=" + str(page_num)
            count = 0
            while True:
                try:
                    self.my_session.headers.update(my_headers)
                    self.my_session.proxies.update(self.proxy_ip)
                    res = self.my_session.get(page_url, timeout=20)
                    if res.status_code != 200:
                        print(res.status_code)
                        self.proxy_pool.remove(self.proxy_ip)
                        self.proxy_ip = self.proxy_pool.get()
                        continue
                    bs_content = BeautifulSoup(res.content, "lxml")
                    component_tags = bs_content.find(name="table", attrs={"class": "SearchResultsTable"}).find_all(
                        name="tr", attrs={"class": re.compile(r"SearchResult")})

                    break
                except Exception as e:
                    count += 1
                    print(sys._getframe().f_code.co_name, e)
                    self.proxy_ip = self.proxy_pool.get()
                    if count > 20:
                        self.proxy_pool._refresh()



            table_header_tags = component_tags[0].find_all(name="th")[11:]

            for component_tag in component_tags[2:]:
                td_tags = component_tag.find_all(name="td")
                try:
                    rough_component_code = td_tags[3].text.strip()
                    no = len(rough_component_code)
                    for num, code_str in enumerate(rough_component_code):
                        if code_str == "\n":
                            no = num
                            break

                    component_code = rough_component_code[:no]
                except Exception as e:
                    print("component code is None", e)
                    continue
                try:
                    component_img = self.mouser_host_url + td_tags[1].find(name="img").get("src").replace("/sm/",
                                                                                                          "/images/")
                except:
                    component_img = ""
                try:
                    rough_attach = td_tags[6].find(name="a", text=re.compile(r".*数据表"))
                    component_attach = rough_attach.get("href")
                    if "http" not in component_attach:
                        component_attach = ""
                except Exception as e:
                    print("pdf is none", page_url, component_code)
                    component_attach = ""
                    # if not component_img:
                    #     continue
                try:
                    component_brand = td_tags[4].a.text
                except Exception as e:
                    print(sys._getframe().f_code.co_name, e)
                    continue

                component = (
                    component_code, component_brand, first_category_name, second_category_name, page_url,
                    component_attach,
                    component_img)
                count = 0
                try:
                    rohs_tag = td_tags[10]
                except Exception as e:
                    print(e)
                    continue

                property_key_values = []
                if rohs_tag.text == "详细信息":
                    key_value = ("RoHS", "Yes")
                    property_key_values.append(key_value)

                len_heads = len(table_header_tags)
                if len_heads:
                    for name_tag, property_tag in zip(table_header_tags, td_tags[-len_heads:]):

                        property_name = name_tag.text.strip()

                        property_value = property_tag.text.strip()
                        key_value = (property_name, property_value)
                        property_key_values.append(key_value)

                while True:
                    try:
                        orcl_conn = OracleSave(1000002)
                        orcl_conn.component_insert(component)
                        for key_value in property_key_values:
                            orcl_conn.properties_insert(key_value)
                        orcl_conn.commit()
                        orcl_conn.conn.close()

                        break
                    except Exception as e:
                        print(e)
                        count += 1
                        # if count > 3:
                        #     break

    def get_page_url(self, category_trees):
        pages_category = []
        for category_tree in category_trees:
            first_category_name = category_tree[0].replace("\ufeff", "")
            second_category_name = str(category_tree[1:-2])
            url, component_count = category_tree[-2:]
            if component_count == 1:
                continue
            for page_num in range(0, int(component_count), 25):
                page_url = url + "?No=" + str(page_num)
                page_category = (first_category_name, second_category_name, page_url)
                pages_category.append(page_category)
        return pages_category

    def page_thread_go(self, page_category):
        first_category_name, second_category_name, page_url = page_category
        count = 0
        my_headers = {'Connection': 'Keep-Alive',
                      'Accept-Language': 'zh-CN,zh;q=0.8',
                      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                      'Accept-Encoding': 'gzip, deflate, sdch',
                      "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
                      "Host": "www.mouser.cn", "Upgrade-Insecure-Requests": "1", }
        while True:
            try:
                self.my_session.headers.update(my_headers)
                self.my_session.proxies.update(self.proxy_ip)
                res = self.my_session.get(page_url, timeout=20)
                if res.status_code != 200:
                    print(res.status_code)
                    self.proxy_pool.remove(self.proxy_ip)
                    self.proxy_ip = self.proxy_pool.get()
                    continue
                bs_content = BeautifulSoup(res.content, "lxml")
                component_tags = bs_content.find(name="table", attrs={"class": "SearchResultsTable"}).find_all(
                    name="tr", attrs={"class": re.compile(r"SearchResult")})

                break
            except Exception as e:
                count += 1
                print(sys._getframe().f_code.co_name, e)
                self.proxy_ip = self.proxy_pool.get()
                if count > 20:
                    self.proxy_pool._refresh()

        table_header_tags = component_tags[0].find_all(name="th")[11:]

        for component_tag in component_tags[2:]:
            td_tags = component_tag.find_all(name="td")
            try:
                rough_component_code = td_tags[3].text.strip()
                no = len(rough_component_code)
                for num, code_str in enumerate(rough_component_code):
                    if code_str == "\n":
                        no = num
                        break

                component_code = rough_component_code[:no]
            except Exception as e:
                print("component code is None", e)
                continue
            try:
                component_img = self.mouser_host_url + td_tags[1].find(name="img").get("src").replace("/sm/",
                                                                                                      "/images/")
            except:
                component_img = ""
            try:
                rough_attach = td_tags[6].find(name="a", text=re.compile(r".*数据表"))
                component_attach = rough_attach.get("href")
                if "http" not in component_attach:
                    component_attach = ""
            except Exception as e:
                print("pdf is none", page_url, component_code)
                component_attach = ""
                # if not component_img:
                #     continue
            try:
                component_brand = td_tags[4].a.text
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                continue

            component = (
                component_code, component_brand, first_category_name, second_category_name, page_url,
                component_attach,
                component_img)
            count = 0
            try:
                rohs_tag = td_tags[10]
            except Exception as e:
                print(e)
                continue

            property_key_values = []
            if rohs_tag.text == "详细信息":
                key_value = ("RoHS", "Yes")
                property_key_values.append(key_value)

            len_heads = len(table_header_tags)
            if len_heads:
                for name_tag, property_tag in zip(table_header_tags, td_tags[-len_heads:]):
                    property_name = name_tag.text.strip()

                    property_value = property_tag.text.strip()
                    key_value = (property_name, property_value)
                    property_key_values.append(key_value)

            while True:
                try:
                    orcl_conn = OracleSave(1000002)
                    orcl_conn.component_insert(component)
                    for key_value in property_key_values:
                        orcl_conn.properties_insert(key_value)
                    orcl_conn.commit()
                    orcl_conn.conn.close()

                    break
                except Exception as e:
                    print("database save exception", e)
                    count += 1
                    # if count > 3:
                    #     break

if __name__ == "__main__":
    mouser_go = MouserGo()
    # multi_category_structures = mouser_go.get_all_category()
    # mouser_go.category_to_csv(multi_category_structures)
    init_multi_category_trees = mouser_go.read_from_csv()

    # multi_category_trees = init_multi_category_trees[270:271]
    for i in range(271, 986, 5):
        multi_category_trees = init_multi_category_trees[i: i+5]

        pages_category = mouser_go.get_page_url(multi_category_trees)
    # print(pages_category)
    # for page_category in pages_category:
    #     mouser_go.page_thread_go(page_category)
        threadingpool = ThreadingPool(16)
        threadingpool.multi_process(mouser_go.page_thread_go, pages_category)
