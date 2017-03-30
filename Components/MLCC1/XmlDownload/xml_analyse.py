"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/24
"""
import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import sys

from Lib.NetCrawl.Constant import Default_Header


class XmlAnalyse:
    def __init__(self):
        self.xml_count = 15
        pass


    def xml_download(self, xml_num):

        while True:
            try:
                my_session = requests.session()
                my_session.headers.update(Default_Header)
                res = my_session.get(("http://www.mlcc1.com/sitemap/sitemap%d.xml" % xml_num))
                if res.status_code == 200:
                    content = res.content.decode()
                    if content:
                        break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
        root = ET.fromstring(content)
        print(root.tag, root.attrib)

        product_urls = []
        for child in root:
            url = child[0].text
            product_urls.append(url)
        return product_urls

    def thread_go(self, parameters):
        url = parameters
        html_analyse = HtmlAnalyse(url)
        bs_content = html_analyse.get_bs_contents()
        tr_tags = bs_content.find(name="tbody").find_all(name="tr")
        for tr_tag in tr_tags:
            td_tags = tr_tag.find_all("td")
            property_name = td_tags[0].text.strip()
            value_tag = td_tags[1]
            if property_name == "料号":
                cc_code = value_tag.text.strip()
            elif property_name == "品牌":
                cc_brandname = value_tag.text.strip()
            elif property_name == "规格书":
                cc_attach = value_tag.get("href")
            property_value = td_tags[1]
        component = (cc_code, cc_brandname, cc_unit, cc_kiname, cc_url, cc_attach, cc_img)


if __name__ == "__main__":
    xml_analyse = XmlAnalyse()
    xml_analyse.xml_download()
