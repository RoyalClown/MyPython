"""
    @description:   
    @author:        RoyalClown
    @date:          2017/5/11
"""
import re
import requests
from bs4 import BeautifulSoup


class GetCompanyList:
    def __init__(self):
        pass

    def get_url(self):
        url = "http://www.digikey.com.cn/search/zh?site=cn&lang=zh"
        res = requests.get(url)
        if res.status_code != 200:
            return

        content = res.content
        bs_content = BeautifulSoup(content, "html.parser")
        ul_tags=bs_content.find_all(name="ul",attrs={"class": "catfiltersub"})
        urls=[]
        for ul_tag in ul_tags:
            url="http://www.digikey.com.cn" + ul_tag.li.a.get("href")
            urls.append(url)
        return urls

if __name__== "__main__":
    lists = GetCompanyList()
    urls = lists.get_url()
    print(urls)
