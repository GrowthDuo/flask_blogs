 # app.py 汇总
from flask import Flask, session, g
import config
from models import UserModel
from exts import db, mail
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from flask_migrate import Migrate
app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)
# 关联蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

# 钩子函数， 正在执行，中间有人插入一脚，先执行插入的，再执行app的
# 如使用 ：before_first_request / before_request / after_request / teardown_request
# 使用钩子函数
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    # 从数据库中获取用户信息
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)

@app.context_processor
def my_context_processor():
   # 返回一个字典，键为"user"，值为g.user
    return {"user": g.user}




if __name__ == '__main__':
    app.run()
