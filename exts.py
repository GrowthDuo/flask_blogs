# 扩展文件，插件
# exts.py 存在的意义是，将一些常用的功能，封装成插件，方便使用，避免循环引用
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
db = SQLAlchemy()
# 创建一个对象
mail = Mail()
