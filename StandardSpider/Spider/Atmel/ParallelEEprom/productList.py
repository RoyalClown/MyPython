"""
    @description:   
    @author:        RoyalClown
    @date:          2016/11/25
"""
import json
import re

import requests

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Atmel.AtmelConstant import Atmel_Pre_Url


class ProductList:
    def __init__(self, url="http://www.atmel.com/zh/cn/products/memories/parallel/parallel_eeprom.aspx"):
        self.url = url

    def get_product_url(self):
        html_analyse = HtmlAnalyse(self.url)
        bs_content = html_analyse.get_bs_contents()
        rough_products = bs_content.find_all(name="div", attrs={"class": "section-devices"})
        img = Atmel_Pre_Url + bs_content.find(name="img", attrs={"src": re.compile(r'/Images/.*?\.jpg')}).get("src")
        imgs_urls = []
        for rough_product in rough_products:
            product_url = Atmel_Pre_Url + rough_product.a.get("href")
            img_url = (img, product_url)
            imgs_urls.append(img_url)
        return imgs_urls


class Detail:
    def __init__(self, img_url):
        self.img, self.url = img_url
        html_analyse = HtmlAnalyse(self.url)
        self.bs_content = html_analyse.get_bs_contents()

    def get_component_list(self):
        url = self.url
        kiname = "Parallel EEPROM"
        img = self.img
        rough_pdf = self.bs_content.find(name="div", attrs={"class": "section-icon-PDF"})
        try:
            attach = Atmel_Pre_Url + rough_pdf.p.a.get("href")
        except:
            attach = ""

        base_properties_names = self.bs_content.find_all(name="div", attrs={"class": "section-parametric1"})
        base_properties_values = self.bs_content.find_all(name="div", attrs={"class": "section-parametric2"})
        base_properties = []
        for base_property_name, base_property_value in zip(base_properties_names, base_properties_values):
            try:
                key = base_property_name.p.text.replace(":", "")
                value = base_property_value.p.text
                base_property = (key, value)
                base_properties.append(base_property)
            except:
                continue

        many_components_properties = []
        try:
            component_list = self.bs_content.find(name="table", attrs={"id": "device-orderingcode-table"}).tbody.find_all(name="tr")
        except:
            code = self.bs_content.find(name="div", id="page-header").h1.text
            component = [url, code, kiname, img, attach]
            single_properties = base_properties[:]
            single_component_properties = (component, single_properties)
            many_components_properties.append(single_component_properties)
            return many_components_properties

        for component in component_list:
            other_properties = component.find_all(name="td")
            order_code = other_properties[0].text
            single_component = [url, order_code, kiname, img, attach]
            single_properties = base_properties[:]
            try:
                package = other_properties[1].a.text
            except:
                package = ""
            single_properties.append(("Package", package))

            operational_range = other_properties[2].text
            single_properties.append(("Operational Range", operational_range))

            carrier_type = other_properties[3].text
            single_properties.append(("Carrier Type", carrier_type))

            atmel_store_availability = other_properties[5].text
            single_properties.append(("Atmel Store Availability", atmel_store_availability))

            unit_price = other_properties[6].text
            single_properties.append(("Unit Price", unit_price))
            single_component_properties = (single_component, single_properties)
            many_components_properties.append(single_component_properties)

        return many_components_properties
