import re

from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse


class SuppliersList:
    def __init__(self):
        pass

    def get_pages_urls(self):
        urls = []
        for i in range(1, 32):
            url = "http://book.youboy.com/sz/dianzi/#page=" + str(i)
            urls.append(url)
        return urls

    def get_supplier_urls(self, url):
        html_analyse = HtmlAnalyse(url)
        bs_content = html_analyse.get_bs_contents()
        ul_tags = bs_content.find_all(name="ul", attrs={"class": "sheng_weizhi_lb"})
        urls = []
        for ul_tag in ul_tags:
            url = "http://book.youboy.com" + ul_tag.div.strong.a.get("href")
            urls.append(url)
        return urls

    def get_supplier(self, url):
        html_analyse = HtmlAnalyse(url)
        bs_content = html_analyse.get_bs_contents()
        ul_tag = bs_content.find(name="ul", attrs={"class": "txl_content_con_L"})
        supplier_name = ul_tag.h1.text.strip()

        supplier_place = ul_tag.li.text.split("：", 2)[1].replace("\n", " ").strip()
        supplier_contact = ul_tag.find(name="li", text=re.compile(r'联系人：')).text.split("：", 2)[1].strip()
        supplier_fax = ul_tag.find(name="li", text=re.compile(r'传真：')).text.split("：", 2)[1].strip()
        supplier_phone = ul_tag.find(name="li", text=re.compile(r'公司	联系电话：')).text.split("：", 2)[1].strip()
        supplier_mobile = ul_tag.find(name="li", text=re.compile(r'手机号码：')).text.split("：", 2)[1].strip()
        supplier_address = ul_tag.find(name="li", text=re.compile(r'联系地址：')).text.split("：", 2)[1].strip()
        line = (supplier_name, supplier_place, supplier_contact, supplier_fax, supplier_phone, supplier_mobile, supplier_address)
        print(line)
        return line

if __name__ == "__main__":
    supplierlist = SuppliersList()
    pages_urls = supplierlist.get_pages_urls()
    lines = []
    for pages_url in pages_urls:
        urls = supplierlist.get_supplier_urls(pages_url)

        # threadingpool = ThreadingPool()
        # threadingpool.multi_process(supplierlist.get_supplier, urls)

        for url in urls:
            line = supplierlist.get_supplier(url)
            lines.append(line)

    with open("I:\PythonPrj\StandardSpider\OtherWork\ShenZhenSupplier\Category.csv", 'w', encoding='utf-8') as f:
        for list_line in lines:
            line = (",".join(list_line)) + "\n"
            f.write(line.encode().decode())
