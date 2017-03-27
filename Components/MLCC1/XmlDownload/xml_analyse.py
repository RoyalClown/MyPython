"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/24
"""
import requests
import sys
import xml.dom.minidom

from Lib.NetCrawl.Constant import Default_Header


class XmlAnalyse:
    def __init__(self):
        pass

    def xml_download(self):

        for num in range(15):
            while True:
                try:
                    my_session = requests.session()
                    my_session.headers.update(Default_Header)
                    res = my_session.get(("http://www.mlcc1.com/sitemap/sitemap%d.xml" % num))
                    if res.status_code == 200:
                        content = res.content.decode()
                        if content:
                            break
                except Exception as e:
                    print(sys._getframe().f_code.co_name, e)
            dom = xml.dom.minidom.parse(content)
            root = dom.documentElement
            xml_tags = root.getElementsByTagName('loc')
            for xml_tag in xml_tags:
                name = xml_tag.data
                print(name)

if __name__ == "__main__":
    xml_analyse = XmlAnalyse()
    xml_analyse.xml_download()
