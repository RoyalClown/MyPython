import requests

from Lib.NetCrawl.Proxy_Pool import ProxyPool

form_data = {
    "class": "040101",
    "classLv": "3",
    "newProductFlg": "false",
    "newProudctHandlingFlg": "false",
    "newSameDayShippedFlg": "false",
    "eventId": "0001",
    "searchType": "2",
    "dispAllFlg": "true",
    "nextSearchIndex": "10",
    "dispPageNo": "1",
    "dispNum": "25",
    "rental": "false",
    "partSameFlg": "false",
    "subWinSearchFlg": "false",
    "used": "false",
}
request_headers = {
    "Accept": "text/html, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "http://www.chip1stop.com",
    "Referer": "http://www.chip1stop.com/web/CHN/zh/search.do?classCd=040101&classLv=3&subWinSearchFlg=false&searchType=2&dispAllFlg=true&searchFlg=false",
    "Host": "www.chip1stop.com",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.14 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}

if __name__ == "__main__":
    proxy_pool = ProxyPool()
    proxy_ip = proxy_pool.get()
    my_session = requests.session()
    my_session.headers.update(request_headers)
    while True:
        try:
            res = my_session.post("http://www.chip1stop.com/web/CHN/zh/search.do?", data=form_data, proxies=proxy_ip)
            print(res.status_code)
            break
        except Exception as e:
            print(e)
            proxy_pool.remove(proxy_ip)
            proxy_ip = proxy_pool.get()
    content = res.content.decode()
    print(content)
