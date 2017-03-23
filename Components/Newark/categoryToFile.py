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


def get_category_url():
    my_headers = Default_Header
    my_headers["host"] = "cn.element14.com"
    my_headers["Upgrade-Insecure-Requests"] = "1"
    while True:
        try:
            # self.proxy_ip = self.proxy_pool.get()
            my_session = requests.session()

            my_session.headers.update(Default_Header)
            # my_session.proxies.update(self.proxy_ip)

            res = my_session.get("http://cn.element14.com/browse-for-products", timeout=20)
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
    category_structures = []
    for first_category_tag in first_category_tags[6:]:
        first_category_name = first_category_tag.li.h2.text.strip()
        second_category_tags = first_category_tag.li.ul.find_all(name="li")
        for second_category_tag in second_category_tags:
            second_category_url = second_category_tag.a.get("href")
            rough_second_category_name = second_category_tag.text.strip()
            flag = re.match(r"(.*?) \((\d+.*?)\)", rough_second_category_name)
            second_category_name = flag.group(1)
            category_structure = (first_category_name.replace(",", "，"), second_category_name.replace(",", "，"), second_category_url)
            category_structures.append(category_structure)

    return category_structures


def csv_write(category_structures):
    with open("..\\Newark.csv", "w", encoding="utf-8") as f:
        for category_structure in category_structures:
            line = (",".join(category_structure)) + "\n"
            f.write(line.encode().decode())


if __name__ == "__main__":
    category_structures = get_category_url()
    csv_write(category_structures)
