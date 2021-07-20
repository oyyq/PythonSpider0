import json
import requests
import pickle                   #方便地将对象写入到文件中，读取时反序列化
import time
from selenium import webdriver
from selenium.webdriver import ActionChains

# 模拟豆瓣的注册过程
def register():
    username = ""
    password = ""
    url = "https://accounts.douban.com/j/mobile/login/verify_phone_code"
    header = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
    }

    postdata = {
        "ck":"",
        "area_code": "+86",
        "number": "19821218557",
        "remember": "true",
        "code": "5451",             # 验证码
        "ticket": "t03E8oqol3DXpi_5pz4wz5H6G9J3bWyljlN6bIHR4ciW-7En6ymtbb1lqy6wtdgqxcDXLPfFPblzK78dBvjvO9kxNtZ55biMENW-2wExfDmAlo*",
        "randstr":"@wx3",
        "tc_app_id":"2044348370"
    }


    res = requests.post(url, data=postdata, headers = header)
    res_data = json.loads(res.text)
    print(res_data)
    if res_data:
        print(res_data['status'])


# selenium模拟豆瓣的登录过程
douban_url =  "https://www.douban.com/"
browser = webdriver.Chrome(executable_path="/Users/ouyangyunqing/Documents/Python/ChromeDriver/chromedriver")




def login():
    username = "19821218557"
    passwd = "oy0419mj"
    browser.get(douban_url)
    time.sleep(3)
    # login_ele 是iframe中的元素, iframe中的元素是用find_element_by_xpath取不到的，要先switch_to
    browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    login_ele = browser.find_element_by_xpath("//li[@class='account-tab-account']")
    login_ele.click()


    username_ele = browser.find_element_by_xpath("//input[@id='username']")
    username_ele.send_keys(username)
    password_ele = browser.find_element_by_xpath("//input[@id='password']")
    password_ele.send_keys(passwd)

    submit_btn = browser.find_element_by_xpath("//a[@class='btn btn-account btn-active']")
    submit_btn.click()

    time.sleep(5)
    # TODO : 滑块验证码的识别
    # cookies = browser.get_cookies()
    # cookie_dict = {}
    # for item in cookies:
    #     cookie_dict[item["name"]] = item["value"]
    # requests.get(douban_url, cookies=cookie_dict)

    #print(browser.get_cookies())



if __name__ == "__main__":
    login()



