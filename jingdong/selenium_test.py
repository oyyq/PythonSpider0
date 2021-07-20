from selenium import webdriver
import time
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException


# 安装chrome driver
chrome_browser = webdriver.Chrome(executable_path="/Users/ouyangyunqing/Documents/Python/ChromeDriver/chromedriver")
#fox_browser = webdriver.Chrome()
chrome_browser.get("https://item.jd.com/100021782266.html")

#拿到页面运行完js之后的html
#print(chrome_browser.page_source)
#time.sleep(30)

try:
    click_ele = chrome_browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
    click_ele.click()
except NoSuchElementException as e:
    pass

#取出点击"商品评价"后的网页源代码
sel = Selector(text=chrome_browser.page_source)
chrome_browser.close()

# click_ele = chrome_browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
# click_ele.click()
# pass