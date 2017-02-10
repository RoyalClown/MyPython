import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType

from Lib.DBConnection.MongoConnection import MongoConnection


def supplier_verification(self, old_urls, urls=None):
    other_urls = []
    for my_url in urls:
        # def thread_go(my_url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.101 Safari/537.36")

        while True:
            driver = webdriver.PhantomJS(
                executable_path='C:\\Users\\RoyalClown\\Desktop\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe',
                desired_capabilities=dcap)
            driver.set_page_load_timeout(5)
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.MANUAL
            proxy.http_proxy = self.proxy_ip
            proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

            try:
                driver.get(my_url)
            except Exception as e:
                print(e)
                continue
            time.sleep(3)
            contents = driver.page_source
            print(contents)
            driver.quit()
            bs_content = BeautifulSoup(contents, "lxml")

            # 以company为前缀的为企业信息
            company = {}

            # 头部信息
            div_tag = bs_content.find(name="div", attrs={"class": "company_info_text"})
            if div_tag:
                company_name = div_tag.p.text.strip()
                break
            else:
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
                continue
        company_tel = div_tag.find(name="img", attrs={
            "src": "http://static.tianyancha.com/wap/images/com_phone.png"}).parent.text.replace("电话:", "").replace(
            "暂无", "").strip()
        company_mail = div_tag.find(name="img", attrs={
            "src": "http://static.tianyancha.com/wap/images/com_mail.png"}).parent.text.replace("邮箱:", "").replace("暂无",
                                                                                                                   "").strip()
        company_web = div_tag.find(name="img", attrs={
            "src": "http://static.tianyancha.com/wap/images/com_web.png"}).parent.text.replace("网址:", "").replace("暂无",
                                                                                                                  "").strip()
        company_address = div_tag.find(name="img", attrs={
            "src": "http://static.tianyancha.com/wap/images/com_adrss.png"}).parent.text.replace("地址:", "").replace(
            "暂无", "").strip()
        company["企业名称"] = company_name
        company["电话"] = company_tel
        company["邮箱"] = company_mail
        company["网址"] = company_web
        company["地址"] = company_address

        # 中间信息

        company_represent = bs_content.find(name="a", attrs={"ng-if": "company.baseInfo.legalPersonName"}).text.strip()
        company_finance = bs_content.find(name="td", attrs={"class": "td-regCapital-value"}).text.strip()
        company_status = bs_content.find(name="td", attrs={"class": "td-regStatus-value"}).text.strip()
        company_regist_time = bs_content.find(name="td", attrs={"class": "td-regTime-value"}).text.strip()

        company["法定代表人"] = company_represent
        company["注册资本"] = company_finance
        company["状态"] = company_status
        company["注册时间"] = company_regist_time

        # 下方信息
        other_div_tags = bs_content.find_all(name="div", attrs={"class": re.compile(r"c8")})

        for other_div_tag in other_div_tags[1:]:
            company_key_value = other_div_tag.text.split("：", 1)
            company_key = company_key_value[0].strip()
            company_value = company_key_value[1].strip()
            company[company_key] = company_value

        mongo_conn = MongoConnection()
        mongo_conn.db_create(company)

        other_company_tags = bs_content.find_all(name="a", attrs={"class": "company_item ng-binding ng-scope"})
        for other_company_tag in other_company_tags:
            other_url = self.host + other_company_tag.get("href")
            if len(other_urls) > 10:
                break
            if other_url not in old_urls:
                other_urls.append(other_url)

    # threading_pool = ThreadingPool()
    # threading_pool.multi_thread(thread_go, urls)

    return other_urls