import urllib.request

import requests
from bs4 import BeautifulSoup
import urllib

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {'User-Agent': User_Agent}


class Proxy:
    # 从西刺网获取一组代理IP地址
    def get_proxy_ip(self):
        proxy_ = []

        url = 'http://www.xicidaili.com/nn/1'
        req = urllib.request.Request(url, headers=header)
        res = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(res, "html.parser")
        ips = soup.findAll('tr')
        for x in range(1, len(ips)):
            try:
                ip = ips[x]
                tds = ip.findAll("td")
                ip_temp = tds[1].contents[0] + "\t" + tds[2].contents[0]
                proxy_.append(ip_temp)
            except:
                continue
        return proxy_

    # 测试代理IP是否有效，延时小于3s
    def validate_ip(self):
        url = "http://www.baidu.com"
        proxy_ = self.get_proxy_ip()
        for i in range(0, len(proxy_)):
            try:
                ip = proxy_[i].strip().split("\t")
                proxy_host = "http://" + ip[0] + ":" + ip[1]
                proxy_temp = {"http": proxy_host}
                res = requests.get(url, timeout=3, proxies=proxy_temp)
                print(proxy_[i])
                return proxy_temp
            except Exception as e:
                continue


if __name__ == '__main__':
    proxy = Proxy()
    proxy.validate_ip()
