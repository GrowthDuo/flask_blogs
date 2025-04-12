from functools import wraps
from flask import g, redirect, url_for

# 装饰器
def login_required(func):
    """
    登录装饰器，用于限制只有已登录用户才能访问页面
    """
    # 保留func信息
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user is None:  # 如果用户未登录
            return redirect(url_for('auth.login'))  # 重定向到登录页面
        else:
            return func(*args, **kwargs)  # 执行原始函数
    return inner
