from flask import Blueprint, request, render_template, g, redirect, url_for

from exts import db
from .forms import QueryForm
from models import QuestionModel
from decorators import login_required

# qa 文章页面，位于根路径，首页
# 定义蓝图名字,url_prefix 路由前缀
bp = Blueprint('qa', __name__, url_prefix='/')

@bp.route('/')
def index():
    # 根据时间倒序排序，获取所有问题,最新的问题排在前面
    question = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('index.html', questions=question)

# 发布问答
@bp.route('/qa/publish/', methods=['GET', 'POST'])
@login_required
def public_question():

    if request.method == 'GET':
        return render_template('public_question.html')
    else:
        form = QueryForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # todo 发布成功后，跳转到文章详情页
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for('qa.public_question'))

#  问答详情
@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template('detail.html', question=question)

