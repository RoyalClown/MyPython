"""
    @description:   属性值处理规则
    @author:        RoyalClown
"""


import re


class PropertyValueModify:

    def double_with_unit(self, crawl_val):
        rough_val = crawl_val.replace(' ', '')
        flag = re.match(r"(^(\+|-)?\d+(\.\d+)?)(\D.*?)(~|～)((\+|-)?\d+(\.\d+)?)(\D.*?)$", rough_val)
        # pv_min = flag.group(1)
        # pv_max = flag.group(6)
        return flag

    def double_without_unit(self, crawl_val):
        rough_val = crawl_val.replace(' ', '')
        flag = re.match(r"(^(\+|-)?\d+(\.\d+)?)(~|～)((\+|-)?\d+(\.\d+)?)$", rough_val)
        # pv_min = flag.group(1)
        # pv_max = flag.group(2)
        return flag

    # 数值为group1，单位为group3
    def single_with_unit(self, crawl_val):
        rough_val = crawl_val.replace(' ', '')
        flag = re.match(r"^((\+/-)|(＜)|(≠)|(＞)|(≥)|(≤))?((\+|-)?(\d+(\.\d+)?))(\D.*?)$", rough_val)

        return flag

    def single_without_unit(self, crawl_val):
        rough_val = crawl_val.replace(' ', '')
        flag = re.match(r'^((\+/-)|(＜)|(≠)|(＞)|(≥)|(≤))?((\+|-)?(\d+(\.\d+)?))$', rough_val)
        return flag

if __name__ == "__main__":
    propertyvaluemodify = PropertyValueModify()
    print(propertyvaluemodify.double_with_unit("-16%~-20%").group(6))

# flag = re.match(r"^(\+/-)?((\+|-)?(\d+(\.\d+)?))(\D.*?)$", rough_val)
#
# flag = re.match(r"^(\+/-)|(＜)|(≠)|(＞)|(≥)|(≤)((\+|-)?(\d+(\.\d+)?))(\D.*?)$", rough_val)
#
# flag = re.match(r"^(\+/-)?((\+|-)?(\d+(\.\d+)?))(\D.*?)$", rough_val)

