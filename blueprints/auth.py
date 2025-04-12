import random

import redis
from flask_mail import Message
from models import emailModel, UserModel
from flask import Blueprint, render_template, jsonify, redirect, url_for,session
from exts import mail, db
from flask import request
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash,check_password_hash
# auth  用户相关的
# 定义蓝图名字,url_prefix 路由前缀
bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        # 验证用户提交的邮箱和密码是否正确
        form = LoginForm(request.form)
        if form.validate():
            # 验证成功
            email = form.email.data
            password = form.password.data
        #     从数据库查找
        #     根据邮箱查找
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在")
                return redirect(url_for("auth.login"))
        #   验证密码
            if check_password_hash(user.password, password):
              #  使用cookie保存用户信息
              # cookie 一般用来存储登录授权的东西，使用session存储用户信息
              # session 存储一些用户信息，比如用户名，头像，用户权限等
              # flask 中是使用session进行加密 存储在cookie中
              session['user_id'] = user.id
              return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))

# 注册蓝图
# get 从服务器中获取数据， post 将客服端向服务器提交数据
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 验证用户提交的邮箱和验证码是否正确
        # 表单验证 ：flask-wtf
        # 使用request.form获取前端表单数据
        # 将拿到的前端数据进行验证
        register_form = RegisterForm(request.form)
        # 自动验证
        #validate = register_form.validate()
        # 验证通过
        if register_form.validate():
            # return "success"
            # 将用户信息存储在数据库中
            # 先获取用户输入的信息
            email = register_form.email.data
            username = register_form.username.data
            password = register_form.password.data
            # 将密码加密
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            # 添加到数据库中
            db.session.add(user)
            db.session.commit()
            # 跳转到登录页面
            # url_for : 动态生成url
            return redirect(url_for('auth.login'))
        # 验证不通过
        else:
            print(register_form.errors)
            # return "error"
            # 返回注册页面
            return redirect(url_for('auth.register'))


# 退出蓝图
@bp.route('/logout')
def logout():
    # 清除session
    session.clear()
    return redirect('/')

# 发送邮箱
@bp.route('/number/email')
def email():
    Email =request.args.get('email')
    # 使用4位数字当作验证码
    code = '%04d' % random.randint(1000, 9999)
    print(code)
    # 发送邮件
    message = Message(subject="注册验证码", recipients=[Email], body="您的验证码是：%s" % code)
    mail.send(message)
    # 验证码临时存入redis，并设置过期时间用于验证,后期更换
    # 现在使用临时方案，数据库存储
    email_model = emailModel(email=Email, code=code)
    db.session.add(email_model)
    db.session.commit()
    # 返回 RESTFUL API 格式
    # 数据格式 {code : 200/400/500, message: '200', data}
    return jsonify({"code": 200, "message": "连接成功", "data": None})


# # 邮箱测试
# @bp.route('/email/test')
# def email_test():
#     # 参数1：邮箱主题  参数2： 收件人列表  参数3：邮件内容
#     message = Message(subject="测试邮箱主题", recipients=["2720891610@qq.com"], body="测试邮件内容：小仙女你好啊！")
#     mail.send(message)
#     return "邮件发送成功"