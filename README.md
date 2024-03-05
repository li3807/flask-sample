# Flask 教程

## 第一章 Hello,Flask!

### 安装 Anaconda 虚拟环境

官方网站[下载](https://www.anaconda.com/download)，Anaconda是一个开源的专注于数据分析的Python发行版本，包含了conda、Python等190多个科学包及其依赖项，
下载安装后，打开 Anaconda Prompt 执行命令

```bash
# 创建一个虚拟环境，名称为  flask-dev python 版本为 3.10 
conda create -n flask-dev python=3.10
# 激活创建的虚拟环境
conda activate flask-dev
```

### 安装 Flask

在激活创建的 flask-dev环境后，执行 pip 命令进行安装，并会安装依赖包

```bash
pip install flask
...
Installing collected packages: MarkupSafe, itsdangerous, colorama, blinker, Werkzeug, Jinja2, click, flask
Successfully installed Jinja2-3.1.3 MarkupSafe-2.1.5 Werkzeug-3.0.1 blinker-1.7.0 click-8.1.7 colorama-0.4.6 flask-3.0.2 itsdangerous-2.1.2
```

### Flask 是什么

追溯到最初，Flask 诞生于 Armin Ronacher 在 2010 年愚人节开的一个玩笑。后来，它逐渐发展成为一个成熟的 Python Web
框架，越来越受到开发者的喜爱。目前它在 GitHub 上是 Star 数量最多的 Python Web 框架，没有之一。根据 2018、2019、2020、2021
连续四年的《Python 开发者调查报告》统计数据，它也是目前最流行的 Python Web 框架。

Flask 是典型的微框架，作为 Web 框架来说，它仅保留了核心功能：请求响应处理和模板渲染。这两类功能分别由 Werkzeug（WSGI 工具库）完成和
Jinja（模板渲染库）完成，因为 Flask 包装了这两个依赖，我们暂时不用深入了解它们。

### 主页

创建 app.py 文件，我们需要创建一个简单主页，主页的 URL 一般就是根地址，即 /。当用户访问根地址的时候，我们需要返回一行欢迎文字。这个任务只需要下面几行代码就可以完成：

```python
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Welcome to My Flask!'


if __name__ == "__main__":
    app.run()
```

在命令行执行 python app.py 即可启动

```bash
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

在浏览器访问 http://127.0.0.1:5000 就可以看到页面输出 Welcome to My Flask!

### 分解程序

下面我们来分解这个 Flask 程序，了解它的基本构成。

首先我们从 flask 包导入 Flask 类，通过实例化这个类，创建一个程序对象 app：

```python
from flask import Flask

app = Flask(__name__)
```

接下来，我们要注册一个处理函数，这个函数是处理某个请求的处理函数，Flask 官方把它叫做视图函数（view funciton），你可以理解为“请求处理函数”。
所谓的“注册”，就是给这个函数戴上一个装饰器帽子。我们使用 app.route() 装饰器来为这个函数绑定对应的 URL，当用户在浏览器访问这个
URL 的时候，就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口：

```python
@app.route('/')
def hello():
    return 'Welcome to My Flask!'
```

填入 app.route() 装饰器的第一个参数是 URL 规则字符串，这里的 /指的是根地址。
创建入口函数，在入口函数中执行启动内置的开发服务器来运行程序。

```python
if __name__ == "__main__":
    app.run()
```

# 第二章 模板

在一般的 Web 程序里，访问一个地址通常会返回一个包含各类信息的 HTML
页面。因为我们的程序是动态的，页面中的某些信息需要根据不同的情况来进行调整，比如对登录和未登录用户显示不同的信息，所以页面需要在用户访问时根据程序逻辑动态生成。

我们把包含变量和运算逻辑的 HTML 或其他格式的文本叫做模板，执行这些变量替换和逻辑计算工作的过程被称为渲染，这个工作由我们这一章要学习使用的模板渲染引擎——Jinja2
来完成。

按照默认的设置，Flask 会从程序实例所在模块同级目录的 templates 文件夹中寻找模板，我们的程序目前存储在项目根目录的 app.py
文件里，所以我们要在项目根目录创建这个文件夹：

```bash
$ mkdir templates
```

## 模板基本语法

在社交网站上，每个人都有一个主页，借助 Jinja2 就可以写出一个通用的模板：

```html
<h1>{{ username }}的个人主页</h1>
{% if bio %}
<p>{{ bio }}</p>  {# 这里的缩进只是为了可读性，不是必须的 #}
{% else %}
<p>自我介绍为空。</p>
{% endif %}  {# 大部分 Jinja 语句都需要声明关闭 #}
```

Jinja2 的语法和 Python 大致相同，你在后面会陆续接触到一些常见的用法。在模板里，你需要添加特定的定界符将 Jinja2
语句和变量标记出来，下面是三种常用的定界符：

- {{ ... }} 用来标记变量。
- {% ... %} 用来标记语句，比如 if 语句，for 语句等。
- {# ... #} 用来写注释。
  模板中使用的变量需要在渲染的时候传递进去。

## 编写主页模板

我们先在 templates 目录下创建一个 index.html 文件，作为主页模板。主页需要显示电影条目列表和个人信息，代码如下所示：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ name }}'s Watchlist</title>
</head>
<body>
<h2>{{ name }}'s Watchlist</h2>
{# 使用 length 过滤器获取 movies 变量的长度 #}
<p>{{ movies|length }} Titles</p>
<ul>
    {% for movie in movies %} {# 迭代 movies 变量 #}
    <li>{{ movie.title }} - {{ movie.year }}</li>
    {# 等同于 movie['title'] #}
    {% endfor %} {# 使用 endfor 标签结束 for 语句 #}
</ul>
<footer>
    <small>&copy; 2018 <a href="http://helloflask.com/book/3">HelloFlask</a></small>
</footer>
</body>
</html>
```

为了方便对变量进行处理，Jinja2 提供了一些过滤器，语法形式如下：

```html
{{ 变量|过滤器 }}
```

左侧是变量，右侧是过滤器名。比如，上面的模板里使用 length 过滤器来获取 movies 的长度，类似 Python 里的 len() 函数。
提示 访问 https://jinja.palletsprojects.com/en/3.0.x/templates/#builtin-filters 查看所有可用的过滤器。

### 准备虚拟数据

为了模拟页面渲染，我们需要先创建一些虚拟数据，用来填充页面内容：

```python
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
```

### 渲染主页模板

使用 render_template() 函数可以把模板渲染出来，必须传入的参数为模板文件名（相对于 templates 根目录的文件路径），这里即 '
index.html'。为了让模板正确渲染，我们还要把模板内部使用的变量通过关键字参数传入这个函数，如下所示：

```python
from flask import Flask, render_template


# ...

@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)
```

在传入 render_template() 函数的关键字参数中，左边的 movies 是模板中使用的变量名称，右边的 movies 则是该变量指向的实际对象。这里传入模板的
name 是字符串，movies 是列表，但能够在模板里使用的不只这两种 Python 数据结构，你也可以传入元组、字典、函数等。

render_template() 函数在调用时会识别并执行 index.html 里所有的 Jinja2
语句，返回渲染好的模板内容。在返回的页面中，变量会被替换为实际的值（包括定界符），语句（及定界符）则会在执行后被移除（注释也会一并移除）。

# 第三章 静态文件

静态文件（static files）和我们的模板概念相反，指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。

在 Flask 中，我们需要创建一个 static 文件夹来保存静态文件，它应该和程序模块、templates 文件夹在同一目录层级，所以我们在项目根目录创建它：

```bash
mkdir static
```

## 生成静态文件 URL

在 HTML 文件里，引入这些静态文件需要给出资源所在的 URL。为了更加灵活，这些文件的 URL 可以通过 Flask 提供的 url_for() 函数来生成。

url_for() 函数的用法，传入端点值（视图函数的名称）和参数，它会返回对应的 URL。对于静态文件，需要传入的端点值是 static，同时使用
filename 参数来传入相对于 static 文件夹的文件路径。
我们在 static 文件夹的根目录下面放了一个 foo.jpg 文件，下面的调用可以获取它的 URL：

```html
<img src="{{ url_for('static', filename='foo.jpg') }}">
```

## 添加 Favicon

Favicon（favourite icon） 是显示在标签页和书签栏的网站头像。你需要准备一个 ICO、PNG 或 GIF 格式的图片，大小一般为
16×16、32×32、48×48 或 64×64 像素。把这个图片放到 static 目录下，然后像下面这样在 HTML 模板里引入它：

```html

<head>
    ...
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
</head>

```

## 添加 CSS

虽然添加了图片，但页面还是非常简陋，因为我们还没有添加 CSS 定义。下面在 static 目录下创建一个 CSS 文件 style.css，内容如下：

```css
/* 页面整体 */
body {
    margin: auto;
    max-width: 580px;
    font-size: 14px;
    font-family: Helvetica, Arial, sans-serif;
}

/* 页脚 */
footer {
    color: #888;
    margin-top: 15px;
    text-align: center;
    padding: 10px;
}

/* 头像 */
.avatar {
    width: 40px;
}

/* 电影列表 */
.movie-list {
    list-style-type: none;
    padding: 0;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
}

.movie-list li {
    padding: 12px 24px;
    border-bottom: 1px solid #ddd;
}

.movie-list li:last-child {
    border-bottom:none;
}

.movie-list li:hover {
    background-color: #f8f9fa;
}

/* 龙猫图片 */
.totoro {
    display: block;
    margin: 0 auto;
    height: 100px;
}
```
接着在页面的 <head> 标签内引入这个 CSS 文件：
```html

<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
```