"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/29
"""
import csv
import re

import requests
import sys
from bs4 import BeautifulSoup

from Components.DBSAVE.oracleSave import OracleSave
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.Constant import Default_Header
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class FPNewark:
    def __init__(self):
        self.my_session = requests.session()
        self.proxy_pool = ProxyPool()
        self.proxy_ip = self.proxy_pool.get()
        pass

    def get_category_trees(self, category_trees):
        multi_category_trees = []
        for category_tree in category_trees:
            url = category_tree[-2]
            count = 0
            while True:
                try:
                    self.my_session.proxies.update(self.proxy_ip)
                    res = self.my_session.get(url, timeout=20)
                    if res.status_code != 200:
                        print(res.status_code)
                        continue
                    bs_content = BeautifulSoup(res.content, "lxml")

                    break
                except Exception as e:
                    count += 1
                    print(sys._getframe().f_code.co_name, url, e)
                    self.proxy_ip = self.proxy_pool.get()
                    if count > 100:
                        self.proxy_pool._refresh()

            category_list = bs_content.find(name="ul", attrs={"class": "categoryList"})
            if not category_list:
                print(category_tree)
                multi_category_trees.append(category_tree)
                continue
            else:

                child_category_tags = category_list.find_all(name="a")

                category_trees = []
                for child_category_tag in child_category_tags:
                    child_category_url = child_category_tag.get("href")
                    rough_child_category_tag = child_category_tag.text.strip()
                    flag = re.match(r"(.*?) \((\d+.*?)\)", rough_child_category_tag)
                    child_category_name = flag.group(1)

                    component_count = flag.group(2).replace(",", "")
                    if component_count == '1':
                        continue

                    child_category = [child_category_name, child_category_url, component_count]
                    child_category_tree = list(category_tree)[:-2] + child_category
                    category_trees.append(child_category_tree)
                child_categories = self.get_category_trees(category_trees)
                print(child_categories)
                multi_category_trees += child_categories
            print("Current Count： ", len(multi_category_trees))
        return multi_category_trees

    def get_first_categories(self):
        my_headers = Default_Header
        my_headers["host"] = "www.newark.com"
        my_headers["Referer"] = "http://www.newark.com/"
        my_headers["Upgrade-Insecure-Requests"] = "1"
        while True:
            try:
                self.my_session.headers.update(my_headers)
                self.my_session.proxies.update(self.proxy_ip)

                res = self.my_session.get("http://www.newark.com/browse-for-products", timeout=20)
                if res.status_code != 200:
                    print(res.status_code)
                    continue
                bs_content = BeautifulSoup(res.content, "lxml")
                first_category_tags = bs_content.find_all(name="ul", attrs={"categoryList"})
                break
            except Exception as e:
                print("Part1",sys._getframe().f_code.co_name, e)
                self.proxy_ip = self.proxy_pool.get()

        second_pages = []
        for first_category_tag in first_category_tags:
            first_category_name = first_category_tag.li.h2.text.strip()
            second_category_tags = first_category_tag.li.ul.find_all(name="li")
            for second_category_tag in second_category_tags:
                second_category_url = second_category_tag.a.get("href")
                rough_second_category_name = second_category_tag.text.strip()
                flag = re.match(r"(.*?) \((\d+.*?)\)", rough_second_category_name)
                second_category_name = flag.group(1)

                component_count = flag.group(2).replace(",", "")
                if component_count == '1':
                    continue
                second_page = (first_category_name, second_category_name, second_category_url, component_count)
                second_pages.append(second_page)
        return second_pages

    def csv_write(self, category_structures):
        with open("..\\Newark_test.csv", "w", encoding="utf-8") as f:
            for category_structure in category_structures:
                modify_category_structure = []
                for structure_name in category_structure:
                    modify_structure_name = structure_name.replace(",", "，")
                    modify_category_structure.append(modify_structure_name)
                line = (",".join(modify_category_structure)) + "\n"
                f.write(line.encode().decode())
    #
    def thread_go(self, category_tree):
        my_headers = Default_Header
        my_headers["host"] = "www.newark.com"
        my_headers["Referer"] = "http://www.newark.com/"
        my_headers["Upgrade-Insecure-Requests"] = "1"
        first_category_name = category_tree[0]
        second_category_name = str(category_tree[1:-2])
        url, component_count = category_tree[-2:]
        page_count = int(int(component_count) / 25) + 1
        for page_num in range(1, page_count + 1):
            page_url = url + "/prl/results/" + str(page_num)
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
                    component_tags = bs_content.find(name="table", id="sProdList").tbody.find_all(name="tr")
                    break
                except Exception as e:
                    count += 1
                    print(sys._getframe().f_code.co_name, e)
                    self.proxy_ip = self.proxy_pool.get()
                    if count > 100:
                        self.proxy_pool._refresh()

            for component_tag in component_tags:
                detail_table = component_tag.find(name="table", attrs={"class": "TFtable"})
                td_tags = component_tag.find_all(name="td")
                try:
                    component_code = td_tags[1].text.strip()
                except Exception as e:
                    print("component code is None", e)
                    continue
                try:
                    component_img = td_tags[1].find(name="img", attrs={"class": "productThumbnail"}).get("src")
                except:
                    component_img = ""
                try:
                    rough_attach = td_tags[2].find(name="a", text="数据表")
                    if not rough_attach:
                        rough_attach = td_tags[2].find(name="a", attrs={"class": "prodDetailsAttachment"})
                    component_attach = rough_attach.get("href")
                    if "http" not in component_attach:
                        component_attach = ""
                except Exception as e:
                    component_attach = ""
                    if not component_img:
                        continue
                try:
                    manufacture_description = td_tags[3].a.find_all(name="p")
                    component_brand = manufacture_description[0].text.strip()
                    component_description = manufacture_description[1].text.strip()
                except Exception as e:
                    print(sys._getframe().f_code.co_name, e)
                    continue

                component = (
                    component_code, component_brand, first_category_name, second_category_name, page_url,
                    component_attach,
                    component_img)
                count = 0
                while True:
                    try:
                        orcl_conn = OracleSave(1000003)
                        orcl_conn.component_insert(component)
                        if detail_table:
                            property_tags = detail_table.find_all(name="tr")
                            for property_tag in property_tags:
                                detail_td_tags = property_tag.find_all("td")
                                property_name = detail_td_tags[0].text.strip()
                                property_value = detail_td_tags[1].text.strip()
                                key_value = (property_name, property_value)
                                orcl_conn.properties_insert(key_value)
                        orcl_conn.commit()
                        orcl_conn.conn.close()

                        break
                    except Exception as e:
                        print(e)
                        count += 1
                        # if count > 3:
                        #     break

    def read_from_csv(self):
        csv_categories = []
        with open("..\\Newark_test.csv", "r", encoding="utf-8") as f:
            read = csv.reader(f)
            for line in read:
                print(line)
                csv_categories.append(line)
        return csv_categories

if __name__ == "__main__":
    fp_newark = FPNewark()
    # initial_category_trees = fp_newark.get_first_categories()
    # multi_category_trees = fp_newark.get_category_trees(initial_category_trees)
    # print(multi_category_trees)
    # fp_newark.csv_write(multi_category_trees)
    multi_category_trees = fp_newark.read_from_csv()
    threadingpool = ThreadingPool(8)
    threadingpool.multi_process(fp_newark.thread_go, multi_category_trees)
    # for category_tree in multi_category_trees:
    #     fp_newark.thread_go(category_tree)

