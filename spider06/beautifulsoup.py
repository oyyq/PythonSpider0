import re

from bs4 import BeautifulSoup


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

soup = BeautifulSoup(html, 'html.parser')
#beautifulsoup支持多种解析引擎,
# 1. "html.parser" 2. "lxml" 3. ["lxml-xml"] 4. "xml" 5. "html5lib"
tag = soup.b
print(tag.name)
print(tag.attrs)

#soup被解析完成后, 面临一个问题, 如何解析处html中的元素呢?
#<head>...</head>中的title
title_tag = soup.title          #soup.xx返回Tag类
print(title_tag.string)

print(type(soup.a))                 #拿到第一个a标签, <class 'bs4.element.Tag'>
print(type(soup.find("a")))         #同上
print(soup.find_all("a"))           #拿到所有的div标签

#以下均为bs4.element.Tag类型
tag = soup.find(id="info")
tag = soup.find("a", id="info")
tag = soup.find("a", id=re.compile("post-\d+"))         #regex


#Tag的子元素
# childrens = tag.contents            #Tag.contents    获取直接子元素
# descendants = tag.descendants       #Tag.descendants 获取所有的后代元素
# for child in childrens:             #child可以是bs4.element.Tag or bs4.element.NavigableString
#     if child.name:                  #NavagableString无name属性.
#         print(child.name)


#以下为bs4.element.NavigableString类型
tag = soup.find(string=re.compile("El.*"))
print(tag.string)

#拿到父元素
parent = soup.find("a", {"id":"link1", "class":"sister"}).parent
print(parent.name)


# 找到兄弟元素, 兄弟元素可以是NavigableString, Tag等,
# {"id":"xx", "class":".."}对于"class"这种多值属性, 命中一个属性也可获取.
next_siblings = soup.find("a", {"id":"link2", "class":"sister"}).next_siblings
for sibling in next_siblings:
    if sibling.string:
        print(sibling.string)

previous_siblings = soup.find("a", {"id":"link2", "class":"sister"}).previous_siblings
for sibling in previous_siblings:
    if sibling.string:
        print(sibling.string)


name_tag = soup.find("p", {"class":"name"})
print(name_tag["class"])
print(name_tag["data-bind"])
print(name_tag.get("class"))
