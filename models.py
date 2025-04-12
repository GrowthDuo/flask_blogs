from exts import db
from datetime import datetime
class UserModel(db.Model):
   __tablename__ = 'user'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   # 用户名，不可为空
   username = db.Column(db.String(100), unique=True, nullable=False)
   # 密码，不可为空
   password = db.Column(db.String(200), nullable=False)
   # email，不可为空且唯一
   email = db.Column(db.String(100), nullable=False, unique=True)
   # 记录注册时间
   join_time = db.Column(db.DateTime, default=datetime.now)

# 邮箱验证码 暂存表
class emailModel(db.Model):
   __tablename__ = 'email'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   # email
   email = db.Column(db.String(100), nullable=False)
   # 验证码
   code = db.Column(db.String(100), nullable=False)


  # 发布问答的表
class QuestionModel(db.Model):
   __tablename__ = 'question'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   # 标题
   # 用户名，不可为空
   title = db.Column(db.String(100), nullable=False)
   # 内容
   content = db.Column(db.Text, nullable=False)
   # 记录创建时间
   create_time = db.Column(db.DateTime, default=datetime.now)

#   使用外键，记录是谁发布的。
   author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   # 建立作者与问题之间的关系，通过db.relationship函数实现
   # backref参数用于设置反向引用，表示问题对象可以通过这个属性访问到对应的作者
   author = db.relationship(UserModel, backref='questions')

# 回复信息详情
class AnswerModel(db.Model):
   __tablename__ = 'answer'
   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   # 内容
   content = db.Column(db.Text, nullable=False)
   # 记录创建时间
   create_time = db.Column(db.DateTime, default=datetime.now)
   # 记录回复
   # 外键
   question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
   # 作者
   author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

   # 外键关系
   question = db.relationship(QuestionModel, backref=db.backref('answers', order_by=create_time.desc()))
   author = db.relationship(QuestionModel, backref='answers')