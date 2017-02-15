"""
    @description:   
    @author:        RoyalClown
    @date:          2017/2/14
"""
import requests

from Components.MLCC1.Constant import First_Headers, First_Cookies
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class Detail:
    def __init__(self, second_class):
        self.first_class_name, self.second_class_name, self.url, self.page_count = second_class
        self.proxy_pool = ProxyPool()

        self.proxy_ip = self.proxy_pool.get()

    def get_class_components(self):
        page_urls = map(lambda num: self.url+"&p="+str(num), range(1, self.page_count+1))

        my_headers = First_Headers
        my_cookies = First_Cookies
        for page_url in page_urls:
            print(page_url)
        def get_page_components(page_url):

            my_session = requests.session()
            my_session.headers.update(my_headers)
            my_session.cookies.update(my_cookies)
            while True:
                try:
                    res = my_session.get(page_url)
                    content = res.content.decode()
                    if res.status_code == 200 and content:
                        break
                    else:
                        self.proxy_pool.remove(self.proxy_ip)
                        self.proxy_ip = self.proxy_pool.get()
                except Exception as e:
                    print(e)

            print(content)


if __name__ == "__main__":
    detail = Detail(('电容', 'MLCC', 'http://www.mlcc1.com/search_simple.html?searchkey=&flag=3', 20210))
    detail.get_class_components()

