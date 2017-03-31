"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/7
"""
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse

a = ['a', 'b', 'c', 'd', ['a', 'b']]


def deco_quotation_marks(func):
    def wrapper(str_list):
        modify_str_list = []
        for single_str in str_list:
            modify_str = str(single_str).replace("'", '"')
            modify_str_list.append(modify_str)
        func(modify_str_list)
    return wrapper

@deco_quotation_marks
def prt(str_list):
    print(str_list)

if __name__ == "__main__":
    prt(a)