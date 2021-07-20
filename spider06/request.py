import requests
import re


# res = requests.get("http://www.baidu.com")
# print(res.text)


#get, post, put, patch, delete方法
# requests.post()
# requests.put()
# requests.options()
# requests.patch()
# requests.delete()

# params = {
#     "username" : "bobby",
#     "password" : "bobby"
# }
# res = requests.get('http://127.0.0.1:8000', params=params)
# print(res.text)
# requests.post("http://127.0.0.1:8000", data=params)
# print(res.json())           #将response转成json
# print(res.encoding)


#正则表达式:
#. 匹配任意字符, 不包括"\n"
#^ 匹配开始位置, 多行模式下匹配每一行的开始
#$ 匹配结束位置, 多行模式下匹配每一行的结束
#* 匹配前一个元字符0到多次
#+ 匹配前一个元字符1到多次
#? 匹配前一个字符0次到1次
#{m, n} 匹配前一个元字符m到n次
#\\  转义字符, 其后的字符将失去作为特殊元字符的含义, 如\\.只能匹配.
#[] 字符集, 可匹配其中任意一个字符
#|  逻辑表达式"或", a|b代表可以匹配a 或者 b
#\b 匹配位于单词开始或结束位置的空字符串, 用于匹配单词, 如\bhi\b只匹配"hi"
#\B 匹配位于单词开始或结束位置的非空字符串
#\d 匹配一个数字, 相当于[0-9]
#\D 匹配非数字, 相当于[^0-9]
#\s 匹配任意空白字符, 相当于[ \t\n\r\f\v]
#\S 匹配非空白字符, 相当于[^ \t\n\r\f\v]
#\w 匹配数字, 字母, 下划线中任意一个字符, 相当于[a-zA-Z0-9_]
#\W 匹配非数字, 字母, 下划线中的任意一个字符, 相当于[^a-zA-Z0-9_]
#注意[]中的"-", 有特殊意义, 代表区间



#re.match
#re.search
#re.findall

#提取字符串
info = "姓名: bobby 生日:1987年10月1日 本科:2005年9月1日"
print(re.findall("\d{4}", info))
match_result = re.match(".*生日.*?\d{4}", info)             #正则表达式没有问题, 但是re.match是从字符串开头开始匹配的.
print(match_result.group(0))


#以上还没有达到将1987数字提取出来的效果, 要使用正则表达式分组的概念, "()"扩起来.
match_result = re.search("生日.*?(\d{4}).*本科.*?(\d{4})", info)
print(match_result.group(0), match_result.group(1), match_result.group(2))

#替换
re_result = re.sub("\d{4}", "2019", info)
print(info)             #不改变原始字符串info
print(re_result)        #返回改变后的结果


#搜索
match_result = re.search("生日.*?\d{4}", info)             #re.search不是从字符串开头开始匹配的.
print(match_result.group(0))


#匹配模式
# re.I, 使匹配对大小写不敏感
# re.L, 本地化识别
# re.M, 多行匹配, 影响^和$
# re.S, 使.匹配包括"\n"在内的所有字符
# re.U, 根据Unicode字符集解析字符, 这个标志影响\w, \W, \b, \B
# re.X
name = "my name is Bobby"
print(re.search("bobby", name, re.I).group())            #re.I: ignore case 忽略大小写

name = '''
my name 
is Bobby
'''
print(re.match(".*(bobby)", name,  re.I | re.S | re.M).group(1))