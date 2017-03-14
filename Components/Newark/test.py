"""
    @description:   
    @author:        RoyalClown
    @date:          2017/3/7
"""
import re

a = '安全系统 - 报警门禁 (119)'.strip()
flag = re.match(r"(.*?) \((.*?)\)", a).group(2)
# b = re.match(r"(.*?) \((.*?\))\)$", a).group(1)
print(flag)
