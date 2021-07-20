from scrapy import Selector

#css选择器
#   *                 选择所有节点
#   #container        选择id为container的节点                   #id是单值属性
#   .container        选取所有class包含container的节点           #class是多值属性
#   li a              选取所有li下的所有a节点
#   ul + p            选择ul后面的第一个p元素                    #p是ul的兄弟节点
#   div#container > ul  选取id为container的div的第一个ul子元素
#   ul ~ p              选取与ul相邻的所有p元素
#   a[title]            选取所有有title属性的a元素
#   a[href="http://www.imooc.com"]      选取所有href属性为http://www.imooc.com的a元素
#   a[href*="imooc"]    选取所有href属性包含"imooc"的a元素
#   a[href^="http"]     选取所有href属性以"http"开头的a元素
#   a[href$=".jpg"]     选取所有href属性以".jpg"结尾的a元素
#   input[type=radio]:checked       选择选中的radio的元素
#   div:not(#container)             选取所有id不是container的div属性
#   li:nth-child(3)                 选取第3个li元素
#   tr:nth-child(2n)                第偶数个tr元素


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
teacher_info_tag = sel.css(".teacher_info")   #对应xpath: "descendant-or-self::*[@class and contains(@class, 'teacher_info')]"
info_tag = sel.css("#info_tag")               #"descendant-or-self::*[@id='info_tag']" || "//*[@id='info_tag']"

age = sel.css(".teacher_info > p::text").extract()[0]     #class属性包含'teacher_info'的所有节点的第一个p子节点的text, 返回一个有data属性的Selector, 从中extract出data属性形成一个list
age = sel.css(".teacher_info p:nth-child(2)::text").extract()[0]      #class属性包含'teacher_info'的所有节点的第2个p子节点的text值
#等价写法, css选择器语法的 ">" 与xpath语法的"/"的作用相同
age = sel.css(".teacher_info > p:nth-child(2)::text").extract()[0]
course = sel.css(".teacher_info + p::text").extract()[0]        #获取class属性包含'teacher_info'的节点后面的第一个p元素
#course = sel.css(".teacher_info ~ p::text").extract()[0]       #相邻的p元素
course_url = sel.css("a[href='https://coding.imooc.com/class/200.html']::text").extract()[0]

sibling_p = sel.css("p.name ~ p::text").extract()               #class属性包含'name'的所有p元素的所有相邻p元素的text





