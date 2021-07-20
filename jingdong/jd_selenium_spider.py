import time

from selenium import webdriver
from jdmodels import *
from scrapy import Selector
import json
import re
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException


browser = webdriver.Chrome(executable_path="/Users/ouyangyunqing/Documents/Python/ChromeDriver/chromedriver")

def process_value(nums_str):
    """
    将字符串类型的数字转换成数字
    :param nums_str: 字符串类型的数字, 数字中可能包含'万'
    :return: 成功返回数字, 默认返回0
    """
    nums = 0
    re_match = re.search("(\d+)", nums_str)
    if re_match:
        nums = int(re_match.group(1))
        if '万' in nums_str:
            nums *= 10000

    return nums



def parse_product(product_id):
    browser.get("https://item.jd.com/{}.html".format(product_id))
    sel = Selector(text=browser.page_source)

    #提取商品的基本信息
    product = Product(product_id=product_id)
    name = "".join(sel.xpath("//div[@class='sku-name']/text()").extract()).strip()            #拿到了'\n'
    price = "".join(sel.xpath("//span[@class='price J-p-{}']/text()".format(product_id)).extract()).strip()
    # extract()直接提取出html
    detail = "".join(sel.xpath("//div[@id='detail']//div[@class='tab-con']").extract())
    #商品轮播图, 需要'https'协议
    product_img =sel.xpath("//div[@id='spec-list']//img/@src").extract()
    # "由 京东 发货, 新松联手机旗舰店提供售后服务"
    # "由 京东 发货并提供售后服务"
    # "由xxx从 xx发货并提供售后服务"
    # 针对以上3种情况, 分别分析html
    supplier_info = "".join(sel.xpath("//div[@id='summary-service']").extract()).strip()
    re_match = re.search('<a href="//(.*).jd.com', supplier_info)
    if re_match:
        product.supplier = re_match.group(1)
    else:
        product.supplier = '京东'

    product.name = name
    product.price = float(price)
    product.content = detail
    product.image_list = json.dumps(product_img)     #将list转成字符串

    # 模拟点击规格和包装
    ggbz_ele = browser.find_element_by_xpath("//div[@class='tab-main large']//li[contains(text(), '规格与包装')]")
    ggbz_ele.click()
    time.sleep(5)
    sel = Selector(text=browser.page_source)
    ggbz_detail = "".join(sel.xpath("//div[@id='detail']/div[@class='tab-con']").extract())
    product.ggbz = ggbz_detail


    # 模拟点击商品评价后获取评价的信息
    sppj_ele = browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
    sppj_ele.click()
    # sppj_ele点击后发起网络请求, 等待一段时间后获取其page_source
    time.sleep(5)
    sel = Selector(text=browser.page_source)
    # 基于大量的页面区分析, 元素是否存在, 元素的xpath是什么.
    tag_list = sel.xpath("//div[@class='tag-list tag-available']//span/text()").extract()
    good_rate = int(sel.xpath("//div[@class='percent-con']/text()").extract()[0])
    product.good_rate = good_rate

    # 拿到所有的a标签, summary_as 是 a list of Selector
    summary_as = sel.xpath("//ul[@class='filter-list']/li/a")
    for summary in summary_as:
        name = summary.xpath("./text()").extract()[0]       # 只有一个元素也以list形式返回
        nums = summary.xpath("./em/text()").extract()[0]    # 将nums = '48万+' 转换成数字
        nums = process_value(nums)

        if name == "晒图":
            product.has_image_comment_nums = nums
        elif name == "视频晒单":
            product.has_video_comment_nums = nums
        elif name == "追评":
            product.has_add_comment_nums = nums
        elif name == "好评":
            product.good_comment_nums = nums
        elif name == "中评":
            product.middle_comment_nums = nums
        elif name == "差评":
            product.bad_comment_nums = nums
        elif name == "全部评价":
            product.comment_nums = nums


    exist_product = Product.select().where(Product.product_id == product.product_id)
    if exist_product:
        product.save()
    else:
        product.save(force_insert=True)


    for tag in tag_list:
        re_match = re.match("(.*)\((\d+)\)", tag)
        if re_match:
            tag_name = re_match.group(1)
            nums = int(re_match.group(2))

            #去重
            exist_summarys = ProductEvalSummary.select().where(ProductEvalSummary.product_id == product.product_id,
                                                              ProductEvalSummary.tag == tag_name)
            if exist_summarys:
                summary = exist_summarys[0]
            else:
                summary = ProductEvalSummary(product_id = product.product_id)

            summary.tag = tag_name
            summary.num = nums
            # ProductEvalSummary 有依赖于Product的外键, 插入ProductEvalSummary数据记录时要检查主表Product中的外键关联记录是否存在
            # 这个体现为外键约束
            summary.save()


    # 获取商品的评价信息, 注意评价分页的问题: 查询是否存在下一页评论的链接
    has_next_page = True
    while has_next_page:
        all_evaluates = sel.xpath("//div[@class='comment-item']")
        for item in all_evaluates:
            product_evaluate = ProductEvaluate(product_id=product.product_id)
            evaluate_id = item.xpath("./@data-guid").extract()[0]
            product_evaluate.id = evaluate_id
            product_evaluate.user_head_url = item.xpath(".//div[@class='user-info']//img/@src").extract()[0]
            product_evaluate.user_name = "".join(item.xpath(".//div[@class='user-info']/text()").extract()).strip()

            star = item.xpath("./div[2]/div[1]/@class").extract()[0]
            star = int(star[-1])
            product_evaluate.star = star
            evaluate = "".join(item.xpath("./div[2]/p[1]/text()").extract()[0]).strip()
            product_evaluate.content = evaluate

            image_list = item.xpath("./div[2]//div[@class='pic-list J-pic-list']/a/img/@src").extract()
            video_list = item.xpath("./div[2]//div[@class='J-video-view-wrap clearfix']//video/@src").extract()

            product_evaluate.image_list = json.dumps(image_list)
            product_evaluate.video_list = json.dumps(video_list)


            praised_nums = int(item.xpath(".//div[@class='comment-op']/a[2]/text()").extract()[0])
            comment_nums = int(item.xpath(".//div[@class='comment-op']/a[3]/text()").extract()[0])

            product_evaluate.praised_nums = praised_nums
            product_evaluate.comment_nums = comment_nums

            comment_info = item.xpath(".//div[@class='comment-message']/div[@class='order-info']/span/text()").extract()
            order_info = comment_info[:-1]
            evaluate_time = comment_info[-1]
            product_evaluate.product_info = json.dumps(order_info)
            evaluate_time = datetime.strptime(evaluate_time, '%Y-%m-%d %H:%M')
            product_evaluate.evaluate_time = evaluate_time


            # 保存评价信息
            exist_product_evaluate = ProductEvaluate.select().where(ProductEvaluate.id == product_evaluate.id)
            if exist_product_evaluate:
                product_evaluate.save()
            else:
                product_evaluate.save(force_insert=True)

        try:
            next_page_ele = browser.find_element_by_xpath("//div[@id='comment']//a[@class='ui-pager-next']")
            #next_page_ele.click()    #click()方法有可能报错, 如果next_page_ele被网页其他元素，如浮窗遮挡
            next_page_ele.send_keys("\n")       #发送回车, 保证点选效果
            time.sleep(5)
            sel = Selector(text=browser.page_source)
        except NoSuchElementException as e:
            has_next_page = False





if __name__ == "__main__":
    parse_product(100021782266)