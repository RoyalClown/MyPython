"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/29
"""
import re

import requests
import sys
from bs4 import BeautifulSoup
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
            while True:
                try:
                    self.proxy_ip = self.proxy_pool.get()
                    self.my_session.proxies.update(self.proxy_ip)
                    res = self.my_session.get(url, timeout=20)
                    if res.status_code != 200:
                        print(res.status_code)
                        self.proxy_pool.remove(self.proxy_ip)
                        continue
                    bs_content = BeautifulSoup(res.content, "lxml")

                    break
                except Exception as e:
                    print(sys._getframe().f_code.co_name, url, e)

            category_list = bs_content.find(name="ul", attrs={"class": "categoryList"})
            if not category_list:
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
                multi_category_trees += child_categories
        return multi_category_trees

    def get_first_categories(self):
        my_headers = Default_Header
        my_headers["host"] = "www.newark.com"
        my_headers["Referer"] = "http://www.newark.com/"
        my_headers["Upgrade-Insecure-Requests"] = "1"
        while True:
            try:
                self.proxy_ip = self.proxy_pool.get()

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
                print(sys._getframe().f_code.co_name, e)
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

    def thread_go(self, category_tree):
        cc_kiname = category_tree[0]
        categories = category_tree[1:-2]
        url, component_count = category_tree[-2:]
        page_count = int(int(component_count) / 25) + 1
        while True:
            try:
                html_analyse = HtmlAnalyse(url)

if __name__ == "__main__":
    fp_newark = FPNewark()
    initial_category_trees = fp_newark.get_first_categories()
    multi_category_trees = fp_newark.get_category_trees(initial_category_trees)
    print(multi_category_trees)
    fp_newark.csv_write(multi_category_trees)

"""
    1. 完成rs-online的抓取规则设计，已开始抓取，但目前速度较慢
    2. 整体修改newark类目结构抓取的程序，使之能够全面正确抓取所有类目。
    3. 修改
"""
