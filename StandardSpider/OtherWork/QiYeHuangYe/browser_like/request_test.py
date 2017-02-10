import re
import time

from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.PhantomJS(
    executable_path='C:\\Users\\RoyalClown\\Desktop\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
try:
    driver.get("http://www.tianyancha.com/company/14030996")
    time.sleep(3)
    contents = driver.page_source
    driver.quit()
    bs_content = BeautifulSoup(contents, "lxml")
    div_tag = bs_content.find(name="div", attrs={"class": "company_info_text"})
    company = div_tag.p.text.strip()
    other_div_tags = bs_content.find_all(name="div", attrs={"class": re.compile(r"c8")})
    for other_div_tag in other_div_tags[1:]:
        key_value = other_div_tag.text.split("：", 1)
        key = key_value[0].strip()
        value = key_value[1].strip()
        print(key, value)

except Exception as e:
    print(e)
