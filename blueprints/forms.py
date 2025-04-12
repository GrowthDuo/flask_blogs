# 注册表单
import wtforms
from wtforms.validators import Email, Length,EqualTo

from models import UserModel, emailModel


class RegisterForm(wtforms.Form):
    # 定义了一个名为email的字段，类型为字符串。它有一个验证器validators参数，其中包含一个验证邮箱格式的验证器Email。如果邮箱格式不正确，会返回一个错误消息。
    # StringField ：字符。 验证器validators。 验证邮箱格式的验证器Email。 message ：错误消息。
    email = wtforms.StringField(validators=[Email(message='邮箱格式不正确')])
    # 验证码
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message='请输入正确的验证码')])
    # 用户名
    username = wtforms.StringField(validators=[Length(min=4, max=8, message='用户名长度必须在4-8之间')])
    # 密码
    password = wtforms.StringField(validators=[Length(min=6, max=16, message='密码长度必须在6-16之间')])
    # 确定密码, 使用Equal 验证器，比较两次输入的密码是否一致
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message='两次输入的密码不一致')])

    # 自定义验证
    # 1.邮箱是否已注册。 2. 验证码是否已过期
    # 邮箱是否已注册， field ：如果验证的是邮箱，则field 就是代表邮箱。
    def validate_email(self, field):
        # .data就可以获取到用户输入的值
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            # 自定义错误消息
            raise wtforms.ValidationError(message='邮箱已被注册')
        # 更简
        # if UserModel.query.filter_by(email=field.data).first():
        #     raise wtforms.validators.ValidationError('邮箱已被注册')

    # 验证验证码
    def validate_code(self, field):
        # .data就可以获取到用户输入的值
        captcha = field.data
        # 获取邮箱
        email_data = self.email.data
        # 根据邮箱和验证码进行查找
        captcha_model = emailModel.query.filter_by(email=email_data, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message='邮箱或验证码错误')

class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='邮箱格式不正确')])
    password = wtforms.StringField(validators=[Length(min=6, max=16, message='密码长度必须在6-16之间')])

class QueryForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=2, max=30, message='标题长度必须在5-30之间')])
    content = wtforms.StringField(validators=[Length(min=2, message='内容长度必须不少于2个')])