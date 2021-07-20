# 为什么要用ORM
# 1. 隔离数据库和数据库版本之间的差异
# 2. 便于维护
# 3. orm会提供防sql注入等功能
# 4. 变量传递式的调用更加简单
# orm框架 peewee, django orm, sqlalchemy
from peewee import *
db = MySQLDatabase("spider",
                   host="127.0.0.1",
                   port=3306,
                   user="root",
                   password="oy0419mj")


class Person(Model):
    name = CharField(max_length=20, primary_key=True)          #默认varchar(255)
    birthday = DateField()                                     #mysql中Date类型

    class Meta:
        database = db
        #table_name = "users"       #指定table名


if __name__ == "__main__":
    db.create_tables([Person])