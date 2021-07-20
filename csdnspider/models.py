'''
数据表
'''

from peewee import *
db = MySQLDatabase("spider",
                   host="127.0.0.1",
                   port=3306,
                   user="root",
                   password="oy0419mj")

'''
定义基本表
'''
class BaseModel(Model):
    class Meta:
        database = db

'''
设计表的时候, 有几个重要点:
1. char类型设置最大长度
2. 无法确定CharField()类型的最大长度, 可以设置为Text
3. 对字段进行格式化, 如default=0 和 null = True
4. 字段的constraint, 如index, primary_key 
'''


#帖子, url格式https://bbs.csdn.net/topics/600329960, id:600329960
class Topic(BaseModel):
    #爬虫中需要仔细分析爬取数据的类型, 多分析几个数据
    id = IntegerField(primary_key=True)                 #贴id
    title = CharField(null=True)                        #贴名
    category = CharField(null=True)                     #帖子的分类
    content = TextField(default="")                     #贴内容
    #不同版面, id 是int或是str
    author = CharField()                                #作者名
    create_time = DateTimeField(null=True)              #创建时间  YYYY-MM-DD HH:MM:SS
    answer_time = DateTimeField(null=True)                  #最近回复时间 xx前, MM-DD, YYYY-MM-DD
    answer_nums = IntegerField(default=0)               #回复数
    browse_nums = IntegerField(default=0)               #人气



#每篇帖子的回答
class Answer(BaseModel):
    id = IntegerField(primary_key=True)                 #每篇回答的id
    topic_id = IntegerField()                           #外键
    content = TextField(default="")                     #回答的内容
    author = CharField()                                #答主
    create_time = DateTimeField()                       #回答时间 xx前, MM-DD, YYYY-MM-DD
    praised_nums = IntegerField(default=0)              #回答点赞数



#贴作者信息
class Author(BaseModel):
    id = CharField(primary_key=True)
    name = CharField()                                  #用户名
    avatar = CharField()                                #头像链接
    desc = TextField(default="")                        #描述
    click_num = IntegerField(default=0)                 #访问量
    original_num = CharField()                          #原创数
    rank = CharField()                                  #排名
    fans_num = IntegerField(default=0)                  #粉丝数
    praised_num = IntegerField(default=0)               #点赞数
    comment_num = IntegerField(default=0)               #评论数
    favor_num = IntegerField(default=0)                 #收藏数



if __name__ == "__main__":
    db.create_tables([Topic, Answer, Author])



