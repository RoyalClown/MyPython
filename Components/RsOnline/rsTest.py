"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/20
"""
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse

html_analyse = HtmlAnalyse("http://china.rs-online.com/web/p/igbt-transistors/7965064/")
bs_content = html_analyse.get_bs_contents()
print(bs_content)