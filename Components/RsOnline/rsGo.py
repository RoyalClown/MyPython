"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/14
"""
import re

import sys

from Components.DBSAVE.oracleSave import OracleSave
from Components.RsOnline.Constant import Rs_Pre_Url
from Lib.Currency.ThreadingPool import ThreadingPool
from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Lib.NetCrawl.Proxy_Pool import ProxyPool


class RsGo:
    def __init__(self):
        self.proxy_pool = ProxyPool()
        self.proxy_ip = self.proxy_pool.get()

    def get_second_category(self):
        while True:
            try:

                html_analyse = HtmlAnalyse("http://china.rs-online.com/web/c/pcb-prototyping/pcb-cleaning/", proxy=self.proxy_ip)
                bs_content = html_analyse.get_bs_contents()
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_ip = self.proxy_pool.get()
        first_categories = bs_content.find_all(name="div", attrs={"class": "horizontalMenu sectionUp"})
        second_categories = []
        for first_category in first_categories:
            first_category_name = first_category.span.text
            ul_tags = first_category.find_all(name="ul", attrs={"class": "column1"})
            for ul_tag in ul_tags:
                li_tags = ul_tag.find_all(name="li")
                for li_tag in li_tags:
                    second_category_url = Rs_Pre_Url + li_tag.a.get("href")
                    second_category_name = li_tag.a.text.replace(li_tag.a.span.text, "").strip()
                    second_category = (first_category_name, second_category_name, second_category_url)
                    second_categories.append(second_category)
        return second_categories

    def get_page_url(self, second_category):
        first_category_name, second_category_name, second_category_url = second_category
        while True:
            try:
                html_analyse = HtmlAnalyse(second_category_url, proxy=self.proxy_ip)
                bs_content = html_analyse.get_bs_contents()
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_ip = self.proxy_pool.get()

        ul_tag = bs_content.find(name="ul", attrs={"class": "brcategories"})
        third_category_tags = ul_tag.find_all(name="div", attrs={"class": "rsGARealEstate"})
        for third_category_tag in third_category_tags:
            third_category_name = third_category_tag.a.text
            third_category_url = Rs_Pre_Url + third_category_tag.a.get("href")

            while True:
                try:
                    html_analyse = HtmlAnalyse(third_category_url, proxy=self.proxy_ip)

                    bs_content = html_analyse.get_bs_contents()
                    break
                except Exception as e:
                    print(sys._getframe().f_code.co_name, e)
                    self.proxy_ip = self.proxy_pool.get()
            try:
                page_tag = bs_content.find(name="div", attrs={"class": "viewProdDiv"}).text
            except Exception as e:
                print(third_category_url, e, "找不到page_tag")
                continue
            flag = re.match(r".*?共(.*?)个", page_tag)
            page_count = int(int(flag.group(1).strip()) / 20 + 1)
            for page_num in range(int(page_count)):
                page_url = third_category_url + "?pn=" + str(page_num + 1)
                while True:
                    try:

                        html_analyse = HtmlAnalyse(page_url, proxy=self.proxy_ip)
                        bs_content = html_analyse.get_bs_contents()
                        break
                    except Exception as e:
                        print(sys._getframe().f_code.co_name, e)
                        self.proxy_ip = self.proxy_pool.get()
                component_url_tags = bs_content.find_all(name="a", attrs={"class": "tnProdDesc"})
                page_attributes = []
                for component_url_tag in component_url_tags:
                    component_url = Rs_Pre_Url + component_url_tag.get("href")
                    union_category_name = second_category_name + "---" + third_category_name
                    page_attribute = (first_category_name, union_category_name, component_url)
                    page_attributes.append(page_attribute)
                #
                threadingpool = ThreadingPool(4)
                threadingpool.multi_process(self.thread_go, page_attributes)

                # for page_attribute in page_attributes:
                #     self.thread_go(page_attribute)

            continue

    def thread_go(self, page_attributes):
        cc_unit, cc_kiname, cc_url = page_attributes
        html_analyse = HtmlAnalyse(cc_url)
        while True:
            try:
                bs_content = html_analyse.get_bs_contents()
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)

        brand_tag = bs_content.find(name="span", attrs={"itemprop": "brand"})
        name_tag = bs_content.find(name="span", attrs={"itemprop": "mpn"})

        if not brand_tag or not name_tag:
            return
        cc_brandname = brand_tag.text.strip()

        cc_code = name_tag.text.strip()

        img_tag = bs_content.find(name="img", attrs={"itemprop": "image"})
        if not img_tag:
            cc_img = ""
        else:
            cc_img = Rs_Pre_Url + img_tag.get("src")

        attach_tag = bs_content.find(name="a", attrs={"onclick": re.compile(r"window\.open\('http://docs")})
        if not attach_tag:
            cc_attach = ""
        else:
            attach_name = attach_tag.get("onclick")
            try:
                cc_attach = re.match(r"window\.open\('(.*?\.pdf)'\)", attach_name).group(1)
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                cc_attach = ""

        component = (cc_code, cc_brandname, cc_unit, cc_kiname, cc_url, cc_attach, cc_img)

        # 器件属性
        while True:
            try:
                orcl_conn = OracleSave(1000005)
                orcl_conn.component_insert(component)
                component_properties = []
                tr_tags = bs_content.find_all(name="tr", attrs={"class": re.compile(r"dr-table-row")})
                for tr_tag in tr_tags:
                    td_tags = tr_tag.find_all(name="td")
                    parameter_name = td_tags[1].text
                    parameter_value = td_tags[2].text
                    component_property = (parameter_name, parameter_value)
                    component_properties.append(component_property)

                    orcl_conn.properties_insert(component_property)
                orcl_conn.commit()
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
            finally:
                orcl_conn.conn.close()

    def csv_write(self, category_structures):
        with open("..\\Rs-online.csv", "w", encoding="utf-8") as f:
            for category_structure in category_structures:
                modify_category_structure = []
                for structure_name in category_structure:
                    modify_structure_name = structure_name.replace(",", "，")
                    modify_category_structure.append(modify_structure_name)
                line = (",".join(modify_category_structure)) + "\n"
                f.write(line.encode().decode())

    def get_csv_categories(self):
        while True:
            try:
                html_analyse = HtmlAnalyse("http://china.rs-online.com/web/c/pcb-prototyping/pcb-cleaning/", proxy=self.proxy_ip)
                bs_content = html_analyse.get_bs_contents()
                break
            except Exception as e:
                print(sys._getframe().f_code.co_name, e)
                self.proxy_pool.remove(self.proxy_ip)
                self.proxy_ip = self.proxy_pool.get()
        first_categories = bs_content.find_all(name="div", attrs={"class": "horizontalMenu sectionUp"})
        third_categories = []
        for first_category in first_categories:
            first_category_name = first_category.span.text
            ul_tags = first_category.find_all(name="ul", attrs={"class": "column1"})
            for ul_tag in ul_tags:
                li_tags = ul_tag.find_all(name="li")
                for li_tag in li_tags:
                    second_category_url = Rs_Pre_Url + li_tag.a.get("href")
                    second_category_name = li_tag.a.text.replace(li_tag.a.span.text, "").strip()
                    while True:
                        try:
                            html_analyse = HtmlAnalyse(second_category_url, proxy=self.proxy_ip)
                            bs_content = html_analyse.get_bs_contents()
                            ul_tag = bs_content.find(name="ul", attrs={"class": "brcategories"})

                            break
                        except Exception as e:
                            print(sys._getframe().f_code.co_name, e, second_category_url)
                            self.proxy_pool.remove(self.proxy_ip)
                            self.proxy_ip = self.proxy_pool.get()
                    if ul_tag:
                        third_category_tags = ul_tag.find_all(name="div", attrs={"class": "rsGARealEstate"})
                        for third_category_tag in third_category_tags:
                            third_category_name = third_category_tag.a.text
                            third_category_url = Rs_Pre_Url + third_category_tag.a.get("href")
                            third_category = (first_category_name, second_category_name, third_category_name, third_category_url)
                            print(third_category)
                            third_categories.append(third_category)
                    else:
                        third_category = (first_category_name, second_category_name, second_category_name, second_category_url)
                        print(third_category)
                        third_categories.append(third_category)
        return third_categories


if __name__ == "__main__":
    rs_go = RsGo()
    second_categories = rs_go.get_second_category()
    for second_category in second_categories:
        rs_go.get_page_url(second_category)
