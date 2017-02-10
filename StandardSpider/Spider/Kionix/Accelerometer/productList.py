"""
    @description:   来源:kionix
                    商城品牌:Kionix
                    目标类目:加速度计
                    商城类目:加速计/加速度传感器
                    来源网址:http://zh-cn.kionix.com/parametric/Accelerometers
    @author:        RoyalClown
    @date:          2016/11/17
"""
import re

import requests
from bs4 import BeautifulSoup

from Lib.NetCrawl.HtmlAnalyse import HtmlAnalyse
from Spider.Kionix.KionixConstant import Kionix_Pdf_Pre_Url, Kionix_Product_Pre_Url
from Spider.PanasonicDevice.PanasonicDeviceConstant import Pre_Panasonic_Device_Url
import json


class ProductList:
    def __init__(self, url="http://zh-cn.kionix.com/parametric/Accelerometers"):
        self.url = url

    def get_product_list(self):
        get_url = "http://zh-cn.kionix.com/html/json_req.php?url=http%3A//solr-lb-1878662441.ap-northeast-1.elb.amazonaws.com/solr/solr-slave/select/%3Fstart%3D0%26rows%3D100%26wt%3Djson%26json.nl%3Dmap%26facet%3Don%26facet.mincount%3D1%26facet.field%3DPartNumber_copy%26facet.field%3DPartName_copy%26facet.field%3DProductSupplyStatusText_copy%26facet.field%3DPackageShortCode_copy%26facet.field%3DAxis_num%26facet.field%3DGRange_copy%26facet.field%3DSensitivity_copy%26facet.field%3DNoise_num%26facet.field%3DResolution_copy%26facet.field%3DPackageSize_copy%26facet.field%3DPackagePins_copy%26facet.field%3DPackageType_copy%26facet.field%3DInterfaceOutput_copy%26facet.field%3DWakeUp_copy%26facet.field%3DFifoFiloBuffer_copy%26facet.field%3DOperatingTemperatureMin_num%26facet.field%3DOperatingTemperatureMax_num%26facet.field%3DSupplyVoltage_copy%26facet.field%3DCurrentConsumption_copy%26facet.field%3DPartHighlightText_copy%26sort%3DPS_PartNumber%20asc%26q%3D%28PS_ProductDivisionCode%3A701010%20OR%20PS_ProductGroupCode%3A701010%20OR%20PS_ProductFamilyCode%3A701010%20OR%20PS_ProductTypeCode%3A701010%20OR%20PS_ProductSubTypeCode%3A%20701010%29%20AND%20ProductDisplayFlag_num%3A%5B1%20TO%20*%5D%20AND%20PS_PartStatus%3A60&jsonp_callback=jQuery17103304592033228262_1479346785834&_=1479346786175"
        html_analyse = HtmlAnalyse(get_url)
        rough_data_json = re.match(r'jQuery17103304592033228262_1479346785834\((.*?)\);$',
                                   html_analyse.get_contents()).group(1)
        data_json = json.loads(rough_data_json)
        productlist_json = data_json["response"]["docs"]
        return self.url, productlist_json


class Detail:
    def __init__(self, url, single_json):
        self.url = url
        self.single_json = single_json

    def get_component(self):
        url = self.url
        code = self.single_json["PS_PartNumber"]
        kiname = "加速计/加速度传感器"

        # 图片需要在详细信息网址获取
        detail_url = Kionix_Product_Pre_Url + code

        def get_img(url):
            html_analyse = HtmlAnalyse(url)
            bs_content = html_analyse.get_bs_contents()
            rough_img = bs_content.find(name="img", id="productImageId")
            try:
                img = rough_img.get("src")
            except:
                print("未获取图片", url)
                img = ''
            return img

        img = get_img(detail_url)

        attach = Kionix_Pdf_Pre_Url + self.single_json["PS_DataSheetLink"]

        component = [url, code, kiname, img, attach]
        return component

    def get_attributes(self):
        many_attributes = []
        for name, value in self.single_json.items():
            if value is None or value == "null" or value == "" or isinstance(value, list) or name == 'PS_PartHighlightText':
                continue
            attribute = (name, value,)
            many_attributes.append(attribute)
        return many_attributes


