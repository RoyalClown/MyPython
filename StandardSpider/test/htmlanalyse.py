from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# driver = webdriver.PhantomJS(
    # executable_path='C:\\Users\\RoyalClown\\Desktop\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')

driver = webdriver.Firefox()
driver.get("http://www.rohm.com.cn/web/china/products/-/product/BR24A01AF-WLB(H2)")
a = driver.page_source
driver.close()
bs_content = BeautifulSoup(a)
print(bs_content)