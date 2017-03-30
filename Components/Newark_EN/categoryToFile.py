"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/16
"""
import re

import requests
import sys
from bs4 import BeautifulSoup

from Lib.NetCrawl.Constant import Default_Header


class NewarkCategory:
    def __init__(self):
        # self.proxy_pool = ProxyPool()
        # self.proxy_ip = self.proxy_pool.get()
        self.my_session = requests.session()
        pass

    def get_category_url(self):
        my_headers = Default_Header
        my_headers["host"] = "www.newark.com"
        my_headers["Referer"] = "http://www.newark.com/"
        my_headers["Upgrade-Insecure-Requests"] = "1"
        while True:
            try:
                # self.proxy_ip = self.proxy_pool.get()

                self.my_session.headers.update(my_headers)
                # my_session.proxies.update(self.proxy_ip)

                res = self.my_session.get("http://www.newark.com/browse-for-products", timeout=20)
                if res.status_code != 200:
                    print(res.status_code)
                    # self.proxy_pool.remove(self.proxy_ip)
                    continue
                bs_content = BeautifulSoup(res.content, "lxml")
                first_category_tags = bs_content.find_all(name="ul", attrs={"categoryList"})
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                # self.proxy_pool.remove(self.proxy_ip)
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
                second_page = (first_category_name, second_category_name, second_category_url)
                second_pages.append(second_page)
        return second_pages

    def get_list_pages(self):
        second_pages = self.get_category_url()
        category_structures = []
        for second_page in second_pages:
            first_category_name, second_category_name, second_category_url = second_page
            count = 0
            while True:
                try:
                    res = self.my_session.get(second_category_url)
                    if res.status_code != 200:
                        print(res.status_code)
                        # self.proxy_pool.remove(self.proxy_ip)
                        continue
                    bs_content = BeautifulSoup(res.content, "lxml")
                    third_category_tags = bs_content.find(name="ul", attrs={"categoryList"}).find_all(name="a")
                    break
                except Exception as e:
                    count += 1
                    print(sys._getframe().f_code.co_name, second_category_url, e)
                    if count > 0:
                        third_category_tags = None
                        break

            if not third_category_tags:
                category_structure = (first_category_name.replace(",", "，"), second_category_name.replace(",", "，"), second_category_url.replace(",", "，"))
                category_structures.append(category_structure)
                continue

            for third_category_tag in third_category_tags:
                third_category_url = third_category_tag.get("href")
                rough_third_category_name = third_category_tag.text.strip()
                flag = re.match(r"(.*?) \((\d+.*?)\)", rough_third_category_name)
                third_category_name = flag.group(1)

                component_count = flag.group(2).replace(",", "")
                if component_count == '1':
                    continue

                union_category_name = second_category_name + "---" + third_category_name
                category_structure = (first_category_name.replace(",", "，"), union_category_name.replace(",", "，"), third_category_url)
                category_structures.append(category_structure)

        return category_structures

    def csv_write(self, category_structures):
        with open("..\\Newark.csv", "w", encoding="utf-8") as f:
            for category_structure in category_structures:
                line = (",".join(category_structure)) + "\n"
                f.write(line.encode().decode())


if __name__ == "__main__":
    newark_category = NewarkCategory()
    category_structures = newark_category.get_list_pages()
    newark_category.csv_write(category_structures)
