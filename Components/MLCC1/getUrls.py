"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/14
"""
import re

from Components.MLCC1.Constant import Pre_Url
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class GetUrls:
    def get_first_classes(self, url="http://www.mlcc1.com/search_simplex.html?searchkey="):
        html_analyse = HtmlAnalyse(url)
        bs_content = html_analyse.get_bs_contents()

        first_tag_names = bs_content.find_all(name="p", attrs={"class": "down"})
        first_class_contents = bs_content.find_all(name="ul", attrs={"class": re.compile(r'mlcc_\d+_list')})

        first_classs = []
        for first_tag_name, first_class_content in zip(first_tag_names, first_class_contents):
            first_class_name = re.match(r'(.*?) （.*?', first_tag_name.text).group(1)
            # first_class_name = first_tag_name.text.replace(' ', '')
            first_class = (first_class_name, first_class_content)
            first_classs.append(first_class)

        return first_classs

    def get_second_classes(self, first_class):
        first_class_name, first_class_content = first_class
        second_tags = first_class_content.find_all(name="a")

        second_classes = [('电容', 'MLCC', 'http://www.mlcc1.com/search_simplex.html?searchkey=&flag=3', 20210)]
        for second_tag in second_tags:
            second_class_name = re.match(r'(.*?) （(\d+)条', second_tag.text).group(1)
            page_count = int(int(re.match(r'(.*?) （(\d+)条', second_tag.text).group(2)) / 15 + 1)
            second_class_url = Pre_Url + second_tag.get("href")
            second_class = (first_class_name, second_class_name, second_class_url, page_count)
            second_classes.append(second_class)
        return second_classes


if __name__ == "__main__":
    get_urls = GetUrls()
    first_classes = get_urls.get_first_classes()
    for first_class in first_classes:
        second_classes = get_urls.get_second_classes(first_class)
        print(second_classes)
