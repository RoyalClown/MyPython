import random
import re
from threading import Timer

import requests

from Lib.NetCrawl.Constant import Default_Header


class ProxyPool:
    def __init__(self):
        self._refreshing = False
        self._refresh()
        timer = Timer(300, self._refresh)
        timer.start()

    def _refresh(self):
        if self._refreshing:
            return
        self._refreshing = True
        proxies = []
        api = ""
        # 免费ip
        # api = "http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip"
        # 米扑代理
        apis = (
        "http://proxy.mimvp.com/api/fetch.php?orderid=860170208153000672&num=100&country_group=1&anonymous=5&result_fields=1,2",
        "http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip")
        # 本地代理
        # api = "http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip"
        for api in apis:
            try:
                my_session = requests.session()
                my_session.headers.update(Default_Header)
                res = my_session.get(api)
                proxy_ips = []
                proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', res.text)
                if not len(proxies):
                    continue
                for proxy in proxies:
                    proxy_ip = {"http": proxy}
                    proxy_ips.append(proxy_ip)
                self.proxy_ips = proxy_ips
                print('init ip pool', len(self.proxy_ips))
                self._refreshing = False
                break
            except Exception as e:
                print(e)

    def get(self):
        if len(self.proxy_ips) > 0:
            return random.choice(self.proxy_ips)
        self._refresh()
        return None

    def remove(self, value):
        try:
            self.proxy_ips.remove(value)
        except:
            pass
        if len(self.proxy_ips) <= 0:
            self._refresh()


if __name__ == "__main__":
    proxy_pool = ProxyPool()
