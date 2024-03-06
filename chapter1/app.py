import os

from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]


class UserModel:
    name = "li"


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)


@app.route('/create', methods=['GET', 'POST'])
def create():
    # 表示GET 请求
    if request.method == 'GET':
        return render_template("create.html")
    # 表示 POST 请求
    else:
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input1.')  # 显示错误提示
            flash('Invalid input2.')  # 显示错误提示
            return redirect(url_for('create'))

        # TODO:保存表单数据到数据库
        # 显示成功创建的提示
        flash('Item created.')
        return redirect(url_for('create'))  # 重定向回主页


@app.context_processor
def inject_user():
    user = UserModel()
    return dict(user=user)


# 传入要处理的错误代码
@app.errorhandler(404)
def page_not_found(e):
    """接收异常对象做为参数"""
    return render_template('errors/404.html'), 404  # 返回模板和状态码


if __name__ == "__main__":
    app.run()
