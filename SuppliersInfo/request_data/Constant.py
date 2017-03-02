import re

Company_Urls = ['http://www.tianyancha.com/company/18695545', 'http://www.tianyancha.com/company/26700907',
                'http://www.tianyancha.com/company/632264618', 'http://www.tianyancha.com/company/9745661',
                'http://www.tianyancha.com/company/348603041', 'http://www.tianyancha.com/company/30294773',
                'http://www.tianyancha.com/company/258890183', 'http://www.tianyancha.com/company/5439623',
                'http://www.tianyancha.com/company/2352884316', 'http://www.tianyancha.com/company/16874639',
                'http://www.tianyancha.com/company/182626309', 'http://www.tianyancha.com/company/29587755',
                'http://www.tianyancha.com/company/165436964', 'http://www.tianyancha.com/company/5226527',
                'http://www.tianyancha.com/company/546190769', 'http://www.tianyancha.com/company/393050985',
                'http://www.tianyancha.com/company/25446998', 'http://www.tianyancha.com/company/1074184',
                'http://www.tianyancha.com/company/157452', 'http://www.tianyancha.com/company/2348949757']

TianYan_Headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "Tyc-From": "normal",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
}
TianYan_Detail_Headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "www.tianyancha.com",
    "Tyc-From": "normal",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36",
}

TianYan_Cookies = {
    "TYCID": "ae8b3cda88024698bae7569c946cfc2e",
    "tnet": "183.15.177.163",
    "RTYCID": "a52996f773e34d5d8fe33fbe77024a4e",
    "aliyungf_tc": "AQAAAIqyiH3yjQkAo7EPt2HtoOPrYFlG",
    "_pk_ref.1.e431": "%5B%22%22%2C%22%22%2C1488155453%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D8MY45dUuLowdW5AePGz0DUITtKyJQT6XVBY8T3zsoWKGSwjxTeP1ASF2x9wN5M7m%26wd%3D%26eqid%3D9b03d9c5004d00580000000658b37338%22%5D",
    "_pk_id.1.e431": "52cb68213b157446.1488155453.1.1488155553.1488155453.",
    "_pk_ses.1.e431": "*",
    "Hm_lvt_e92c8d65d92d534b0fc290df538b4758": "1488155455",
    "Hm_lpvt_e92c8d65d92d534b0fc290df538b4758": "1488155553",
    "_utm": "ca24d64d9ef3463a8cded84729bc1cb5",
    "paaptp": "3744d4573918818fbd27ba5370063309edcfaed93c04f6ab0515a7cfbad89"
}

TianYan_Detail_Cookies = {
    "TYCID": "0fcdc37051354129b659bf4c5034ea3b",
    "tnet": "183.15.176.199",
    "RTYCID": "6e24fe2eeb2d407ca167631d6cf04002",
    "aliyungf_tc": "AQAAAOr1HkhznwUAx7APt7KPNYfIkXBq",
    "_pk_ref.1.e431": "%5B%22%22%2C%22%22%2C1486429622%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DTq1E7cHm4uVs5HHHgJ5FDO3a3n6oZr3sGdLN2I0PMOjNhcKvK-ZTiQUmqIjXbaDv%26wd%3D%26eqid%3Dcf6d9184000b6495000000065899136b%22%5D",
    "_pk_id.1.e431": "57758546a4953c28.1486351015.3.1486430893.1486429622.",
    "_pk_ses.1.e431": "*",
    "Hm_lvt_e92c8d65d92d534b0fc290df538b4758": "1486351015,1486426989",
    "Hm_lpvt_e92c8d65d92d534b0fc290df538b4758": "1486430893",
    "_utm": "9b15b2e88e7e44dba2f02bb74fba2660",
}

if __name__ == "__main__":
    import requests
    import time

    my_session = requests.session()
    my_session.headers.update(TianYan_Headers)
    res = my_session.get(
        "http://www.tianyancha.com/tongji/2546208953.json?random=" + str(round(time.time(), 3)).replace(".", ""))
    content = res.content
    random_json = eval(content)
    print(random_json)
    data_v = random_json["data"]["v"]
    print(data_v)

    token = re.match(r".*?token=(.*?);.*?", str(bytes(eval(data_v)))).group(1)
    print(token)

    TianYan_Cookies["token"] = token
    my_session.cookies.update(TianYan_Cookies)
    res = my_session.get("http://www.tianyancha.com/company/2546208953.json")
    content = res.content.decode()
    print(content)
