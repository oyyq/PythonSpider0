from scrapy import Selector

#xpath语法
#1. xpath简介
#   xpath使用路径表达式在xml和html中进行导航, 根据路径表达式定位元素
#   xpath包含标准函数库, 对于支持xpath语法的解析库通用.
#   xpath是一个w3c的标准.
#2. xpath术语
#父节点, 子节点, 先辈节点, 兄弟节点
#3. xpath语法
# 表达式           说明
# article         选取所有article元素的所有子节点
# /article        选取根元素article
# article/a       选取所有属于article的子元素的a元素
# //div           选取所有div子元素(不论出现在html任何地方)
# article//div    选取所有属于article元素的后代的div元素, 不论它出现在article之下的任何位置
# //@class        选取所有名为class的属性
# /article/div[1] 选取属于article子元素的第一个div元素
# /article/div[last()]  选取属于article子元素的最后一个div元素
# /article/div[last()-1]
# //div[@lang]    选取所有拥有lang属性的div元素
# //div[@lang='eng']  选取所有lang属性为eng的div元素
# /div/*
# //div[@*]         选取所有带属性的div元素
# //div/a | //div/p 选取所有div元素的a子元素和p子元素


html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
</body>
</html>
"""

sel = Selector(text=html)
teacher_tag = sel.xpath("//div[@class='teacher_info info']/p")                  #多值属性全量匹配, 返回list
teacher_tag = sel.xpath("//div[contains(@class, 'teacher_info')]/p")            #多值属性class命中teacher_info即匹配
teacher_tag = sel.xpath("//div[contains(@class, 'teacher_info')]/p[last()]/text()")    #最后一个p标签
#last(), text()是xpath的函数, last(): 获取标签列表的最后一个, text(): 获取标签中的文本.
teacher_info_class = sel.xpath("//div[contains(@class, 'teacher_info')]/@class")
#/@class获取class的属性值 返回<Selector xpath="//div[contains(@class, 'teacher_info')]/@class" data='teacher_info info'>
#从这个对象中提取出值, class属性包含'teacher_info'的所有div标签的class属性组成一个list
teacher_info_class = sel.xpath("//div[contains(@class, 'teacher_info')]/@class").extract()[0]
p_tag = sel.xpath("//p[@class='age']|//p[@class='work_years']")                   #class属性等于'age'和class属性等于'work_years'的所有p标签