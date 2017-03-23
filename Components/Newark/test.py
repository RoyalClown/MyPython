"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/7
"""
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse

html_analyse = HtmlAnalyse('https://api.github.com/repos/kennethreitz/requests/git/commits/a050faf084662f3a352dd1a941f2c7c9f886d4ad')
bs_content = html_analyse.get_bs_contents()
print(bs_content)