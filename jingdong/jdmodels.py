from peewee import *

db = MySQLDatabase("JDspider",
                   host="127.0.0.1",
                   port=3306,
                   user="root",
                   password="oy0419mj")

class BaseModel(Model):
    class Meta:
        database = db


# verbose_name: 表字段的注释
class Product(BaseModel):
    product_id = BigIntegerField(primary_key=True, verbose_name="商品ID")
    name = CharField(max_length=500, verbose_name="商品名")
    price = FloatField(verbose_name="商品价格")
    content = TextField(default="", verbose_name="商品描述")
    supplier = CharField(max_length=500, default="", verbose_name="供应商")
    ggbz = TextField(default="", verbose_name="规格和包装")
    image_list = TextField(default="", verbose_name="商品图片序列")

    good_rate = IntegerField(verbose_name="好评率")
    comment_nums = IntegerField(default=0, verbose_name="评论数")
    has_image_comment_nums = IntegerField(default=0, verbose_name="晒图数")
    has_video_comment_nums = IntegerField(default=0, verbose_name="视频晒单数")
    has_add_comment_nums = IntegerField(default=0, verbose_name="追评数")
    good_comment_nums = IntegerField(default=0, verbose_name="好评数")
    middle_comment_nums = IntegerField(default=0, verbose_name="中评数")
    bad_comment_nums = IntegerField(default=0, verbose_name="差评数")


#用户表
class User(BaseModel):
    user_id = IntegerField(primary_key=True, verbose_name="用户ID")
    head_url = CharField(verbose_name="用户头像")
    user_name = CharField(verbose_name="用户名")



# 商品评价表
class ProductEvaluate(BaseModel):
    id = CharField(primary_key=True)             # 为什么不是IntegerField?
    #外键关联Product表
    product_id = ForeignKeyField(Product, Product.product_id, verbose_name="商品")
    #外键关联User表
    user_head_url = CharField(max_length=100, verbose_name="用户头像")
    user_name = CharField(max_length=20)

    product_info = CharField(max_length=500, verbose_name="购买商品配置")
    evaluate_time = DateTimeField(verbose_name="评价时间")
    content = TextField(default="", verbose_name="评价内容")
    star = IntegerField(default=0, verbose_name="评分")
    comment_nums = IntegerField(default=0, verbose_name="评论数")      #对该条评价的一级评论数
    praised_nums = IntegerField(default=0, verbose_name="点赞数")      #对该评价的点赞数
    image_list = TextField(default="", verbose_name="图片")            #评价的图片连接
    video_list = TextField(default="", verbose_name="视频")            #评价的视频链接


class ProductEvalSummary(BaseModel):
    id = IntegerField(primary_key=True)
    product_id = ForeignKeyField(Product, Product.product_id, verbose_name="商品")
    tag = CharField(max_length=20, verbose_name="标签")
    num = IntegerField(default=0, verbose_name="数量")




if __name__ == "__main__":
    db.create_tables([Product, User, ProductEvaluate, ProductEvalSummary])