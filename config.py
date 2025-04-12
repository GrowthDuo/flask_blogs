
SECRET_KEY = 'trhvycpjdpnvdagf'

# 数据库配置信息
HOSTNAME = '127.0.0.1'
PORT = '3306'
USERNAME = 'root'
PASSWORD = '123456'
DATABASE = 'flaskBlog'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# trhvycpjdpnvdagf
# 邮箱配置
MAIL_SERVER ='smtp.qq.com'
# 端口
MAIL_PORT = 465
# 是否加密
MAIL_USE_SSL = True

MAIL_USERNAME = '2016583339@qq.com'
MAIL_PASSWORD = 'trhvycpjdpnvdagf'
MAIL_DEFAULT_SENDER = '2016583339@qq.com'