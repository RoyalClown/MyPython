import random
import re

import requests

from Lib.NetCrawl.Constant import Default_Header


class ProxyPool:
    def __init__(self, flag=True):
        self.flag = flag
        self._refreshing = False
        self._refresh()

    def _refresh(self):
        if self._refreshing:
            return
        self._refreshing = True
        proxies = []
        api = ""
        # 免费ip
        # api = "http://www.66ip.cn/nmtq.php?getnum=800&isp=0&anonymoustype=3&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip"
        # 米扑代理
        api = "http://proxy.mimvp.com/api/fetch.php?orderid=860170208153000672&num=100&country_group=1&anonymous=5&result_fields=1,2"
        # 本地代理
        # api = "http://proxy.mimvp.com/api/fetch.php?orderid=860170208153000672&num=100&country_group=1&anonymous=5&result_fields=1,2"

        try:
            my_session = requests.session()
            my_session.headers.update(Default_Header)
            res = my_session.get(api)
            proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', res.text)
            if not self.flag:
                proxy_ips = proxies
            else:
                proxy_ips = []

                for proxy in proxies:
                    proxy_ip = {"http": proxy}
                    proxy_ips.append(proxy_ip)
            self.proxy_ips = proxy_ips
            # self.proxy_ips = [{'http': '218.4.101.130:83'}, {'http': '1.25.190.88:8888'}, {'http': '220.194.213.242:8080'}, {'http': '117.32.143.150:80'}, {'http': '218.204.60.5:8118'}, {'http': '120.52.73.97:8090'}, {'http': '120.52.73.97:8081'}, {'http': '120.52.73.97:81'}, {'http': '120.52.73.97:8087'}, {'http': '124.88.67.17:82'}, {'http': '125.88.74.122:83'}, {'http': '120.52.73.98:98'}, {'http': '124.88.67.30:83'}, {'http': '101.200.141.114:80'}, {'http': '120.52.73.98:91'}, {'http': '124.88.67.23:843'}, {'http': '120.52.73.97:90'}, {'http': '218.63.208.223:3128'}, {'http': '120.52.73.97:8085'}, {'http': '122.114.60.29:8888'}, {'http': '121.232.145.40:9000'}, {'http': '120.52.73.98:8085'}, {'http': '121.232.144.196:9000'}, {'http': '120.52.73.98:89'}, {'http': '124.133.230.254:80'}, {'http': '124.88.67.19:83'}, {'http': '122.70.211.101:8888'}, {'http': '124.88.67.24:82'}, {'http': '120.52.73.98:8093'}, {'http': '120.52.73.97:99'}, {'http': '120.52.73.98:8087'}, {'http': '1.188.161.60:80'}, {'http': '121.41.8.7:8888'}, {'http': '124.88.67.39:843'}, {'http': '125.95.234.235:8888'}, {'http': '117.21.234.96:8080'}, {'http': '183.61.236.55:3128'}, {'http': '115.200.2.72:80'}, {'http': '117.15.131.112:8888'}, {'http': '115.219.192.21:8118'}, {'http': '119.117.32.109:80'}, {'http': '202.69.71.210:808'}, {'http': '120.52.73.98:8088'}, {'http': '120.52.73.98:8099'}, {'http': '120.52.73.97:89'}, {'http': '124.88.67.10:843'}, {'http': '120.52.73.97:95'}, {'http': '1.29.53.53:80'}, {'http': '101.200.169.110:80'}, {'http': '120.52.73.98:84'}]
            print('init ip pool', len(self.proxy_ips))
            self._refreshing = False
        except:
            self._refresh()

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
