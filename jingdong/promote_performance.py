# 提升selenium性能: 不加载图片
# 无界面启动selenium，无头模式

from selenium.webdriver.chrome.options import Options
from selenium import webdriver

chrome_options = Options()
chrome_options.add_argument('--headless')
# google文档提到加上--disable-gpu属性来规避bug
chrome_options.add_argument('--disable-gpu')
# 以无界面形式开启浏览器
browser = webdriver.Chrome(executable_path="", chrome_options=chrome_options)

# 不加载图片
chrome_options.add_argument('blink-settings=imagesEnabled=false')

#chrome_options.add_argument  https://peter.sh/experiments/chromium-command-line-switches/
#命令行启动chrome: open -a /Applications/Google\ Chrome.app/ -b --enable-features  'http://www.baidu.com'