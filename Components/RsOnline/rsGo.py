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


class RsGo:
    def __init__(self):
        pass

    def get_second_category(self):
        html_analyse = HtmlAnalyse("http://china.rs-online.com/web/")
        bs_content = html_analyse.get_bs_contents()
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
        html_analyse = HtmlAnalyse(second_category_url)
        bs_content = html_analyse.get_bs_contents()
        ul_tag = bs_content.find(name="ul", attrs={"class": "brcategories"})
        third_category_tags = ul_tag.find_all(name="div", attrs={"class": "rsGARealEstate"})
        for third_category_tag in third_category_tags:
            third_category_name = third_category_tag.a.text
            third_category_url = Rs_Pre_Url + third_category_tag.a.get("href")
            html_analyse = HtmlAnalyse(third_category_url)
            data = {
                "AJAXREQUEST": "_viewRoot",
                "j_id2275": "j_id2275",
                "ajax-dimensions": "",
                "ajax-request": "true",
                "ajax-sort-by": "ajax-sort-order",
                "ajax-attrSort": "false",
                "javax.faces.ViewState": "j_id1",
                "j_id2275:j_id2277": "j_id2275:j_id2277",
            }
            bs_content = html_analyse.get_bs_contents()
            page_tag = bs_content.find(name="div", attrs={"class": "viewProdDiv"}).text
            flag = re.match(r".*?共(.*?)个", page_tag)
            page_count = flag.group(1).strip()
            for page_num in range(int(page_count)):
                page_url = third_category_url + "?pn=" + str(page_num)
                html_analyse = HtmlAnalyse(page_url)
                bs_content = html_analyse.get_bs_contents()
                component_url_tags = bs_content.find_all(name="a", attrs={"class": "tnProdDesc"})
                page_attributes = []
                for component_url_tag in component_url_tags:
                    component_url = Rs_Pre_Url + component_url_tag.get("href")
                    page_attribute = (first_category_name, second_category_name, component_url)
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
            cc_attach = re.match(r"window\.open\('(.*?\.pdf)'\)", attach_name).group(1)

        component = (cc_code, cc_brandname, cc_unit, cc_kiname, cc_url, cc_attach, cc_img)

        # 器件属性
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
        orcl_conn.conn.close()


if __name__ == "__main__":
    rs_go = RsGo()
    second_categories = rs_go.get_second_category()
    for second_category in second_categories:
        rs_go.get_page_url(second_category)
