"""
    @description:   
    @author:        RoyalClown
    @date:          2016/12/2
"""
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
)

driver = webdriver.PhantomJS(desired_capabilities=dcap)

driver.get("http://m.iqiyi.com/v_19rrmmdbkg.html")

driver.get_screenshot_as_file('01.png')

driver.quit()
