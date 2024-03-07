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

# 第四章 模板优化

## 自定义错误页面

目前的程序中，如果你访问一个不存在的 URL，比如 /hello，Flask 会自动返回一个 404 错误响应。默认的错误页面非常简陋。在 Flask
程序中自定义错误页面非常简单，我们先编写一个 404 错误页面模板，在 templates 目录下创建 errors 目录，并创建 404.html
文件，如下所示：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>404 's Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>
<body>
<h2>
    <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
    404 's Watchlist
</h2>
<ul class="movie-list">
    <li>
        Page Not Found - 404
        <span class="float-right">
                <a href="{{ url_for('index') }}">Go Back</a>
            </span>
    </li>
</ul>
<footer>
    <small>&copy; 2018 <a href="http://helloflask.com/book/3">HelloFlask</a></small>
</footer>
</body>
</html>
```

接着使用 app.errorhandler() 装饰器注册一个错误处理函数，它的作用和视图函数类似，当 404 错误发生时，这个函数会被触发，返回值会作为响应主体返回给客户端：

```python
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码
```

## 模板上下文处理函数

错误页面模板和主页模板有大量重复的代码，比如 <head>
标签的内容，页首的标题，页脚信息等。这种重复不仅带来不必要的工作量，而且会让修改变得更加麻烦。举例来说，如果页脚信息需要更新，那么每个页面都要一一进行修改。
显而易见，这个问题有更优雅的处理方法，模板上下文处理函数。
对于多个模板内都需要使用的变量，我们可以使用 app.context_processor 装饰器注册一个模板上下文处理函数，如下所示：

```python
class UserModel:
    name = "li"


@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = UserModel()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}
```

修改 404.html 模板页面，可以直接试用 user 变量

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{user.name}} 's Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>
<body>
<h2>
    <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
    {{user.name}}'s Watchlist
</h2>
<ul class="movie-list">
    <li>
        Page Not Found - 404
        <span class="float-right">
                <a href="{{ url_for('index') }}">Go Back</a>
            </span>
    </li>
</ul>
<footer>
    <small>&copy; 2018 <a href="http://helloflask.com/book/3">HelloFlask</a></small>
</footer>
</body>
</html>
```

## 使用模板继承来组织模板

对于模板内容重复的问题，Jinja2 提供了模板继承的支持。这个机制和 Python 类继承非常类似：我们可以定义一个父模板，一般会称之为基模板（base
template）。基模板中包含完整的 HTML 结构和导航栏、页首、页脚等通用部分。在子模板里，我们可以使用 extends 标签来声明继承自某个基模板。

基模板中需要在实际的子模板中追加或重写的部分则可以定义成块（block）。块使用 block 标签创建， {% block 块名称 %} 作为开始标记，{%
endblock %} 或 {% endblock 块名称 %} 作为结束标记。通过在子模板里定义一个同样名称的块，你可以向基模板的对应块位置追加或重写内容。

### 编写基模板

在基模板里，我们添加了两个块，一个是包含 <head></head> 内容的 head 块，另一个是用来在子模板中插入页面主体内容的 content
块。在复杂的项目里，你可以定义更多的块，方便在子模板中对基模板的各个部分插入内容。另外，块的名字没有特定要求，你可以自由修改。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ user.name }}'s Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
    {% endblock head%}
</head>
<body>
<h2>
    <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
    {{ user.name }}'s Watchlist
</h2>
<nav>
    <ul>
        <li><a href="{{ url_for('index') }}">Home</a></li>
    </ul>
</nav>
{% block content %}
{% endblock content%}
<footer>
    <small>&copy; 2018 <a href="http://helloflask.com/book/3">HelloFlask</a></small>
</footer>
</body>
</html>
```

> 因为基模板会被所有其他页面模板继承，如果你在基模板中使用了某个变量，那么这个变量也需要使用模板上下文处理函数注入到模板里。

### 编写子模板

创建了基模板后，子模板的编写会变得非常简单。下面是新的主页模板（index.html）

```html
{% extends 'base/base.html' %}

{% block content %}
<p>{{ movies|length }} Titles</p>
<ul class="movie-list">
    {% for movie in movies %}
    <li>{{ movie.title }} - {{ movie.year }}
        <span class="float-right">
            <a class="imdb" href="https://www.imdb.com/find?q={{ movie.title }}" target="_blank"
               title="Find this movie on IMDb">IMDb</a>
        </span>
    </li>
    {% endfor %}
</ul>
<img alt="Walking Totoro" class="totoro" src="{{ url_for('static', filename='images/totoro.gif') }}" title="to~to~ro~">
{% endblock content%}
```

第一行使用 extends 标签声明扩展自模板 base.html，可以理解成“这个模板继承自 base.html“，接着我们定义了 content
块，这里的内容会插入到基模板中 content 块的位置。
> 默认的块重写行为是覆盖，如果你想向父块里追加内容，可以在子块中使用 super() 声明，即 {{ super() }}

404 错误页面的模板类似，如下所示:

```html
{% extends 'base/base.html' %}

{% block content %}
<ul class="movie-list">
    <li>
        Page Not Found - 404
        <span class="float-right">
            <a href="{{ url_for('index') }}">Go Back</a>
        </span>
    </li>
</ul>
{% endblock content%}
```

# 第五章 表单

在 HTML 页面里，我们需要编写表单来获取用户输入。一个典型的表单如下所示：

```html

<form method="post">  <!-- 指定提交方法为 POST -->
    <label for="name">名字</label>
    <input type="text" name="name" id="name"><br>  <!-- 文本输入框 -->
    <label for="occupation">职业</label>
    <input type="text" name="occupation" id="occupation"><br>  <!-- 文本输入框 -->
    <input type="submit" name="submit" value="登录">  <!-- 提交按钮 -->
</form>
```

编写表单的 HTML 代码有下面几点需要注意：

- 在 ```<form>``` 标签里使用 method 属性将提交表单数据的 HTTP 请求方法指定为 POST。如果不指定，则会默认使用 GET
  方法，这会将表单数据通过 URL 提交，容易导致数据泄露，而且不适用于包含大量数据的情况。
- ```<input>``` 元素必须要指定 name 属性，否则无法提交数据，在服务器端，我们也需要通过这个 name 属性值来获取对应字段的数据

> 填写输入框标签文字的 <label> 元素不是必须的，只是为了辅助鼠标用户。当使用鼠标点击标签文字时，会自动激活对应的输入框，这对复选框来说比较有用。for
> 属性填入要绑定的 ```<input>``` 元素的 id 属性值。

## 创建新条目

创建新条目可以放到一个新的页面来实现，创建 create.html 并继承 base.html 在里面添加一个表单：

```html
{% extends 'base/base.html' %}
{% block content %}
{% for message in get_flashed_messages() %}
<div class="alert">{{ message }}</div>
{% endfor %}
<form method="post" action="/create">
    Name <input type="text" name="title" autocomplete="off" required>
    Year <input type="text" name="year" autocomplete="off" required>
    <input class="btn" type="submit" name="submit" value="Add">
</form>
{% endblock%}
```

在这两个输入字段中，autocomplete 属性设为 off 来关闭自动完成（按下输入框不显示历史输入记录）；另外还添加了 required
标志属性，如果用户没有输入内容就按下了提交按钮，浏览器会显示错误提示。

### 处理表单数据

默认情况下，当表单中的提交按钮被按下，浏览器会创建一个新的请求，默认发往当前 URL（在 <form> 元素使用 action 属性可以自定义目标
URL）,我们需要创建 create 的路由地址：

```python
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
        return redirect(url_for('create'))  
```

为了能够处理 POST 请求，在使用 ```@app.route ```装饰器，增加 methods 属性，配置为 ['GET', 'POST'] 表示支持GET 和 POST 请求。
两种方法的请求有不同的处理逻辑：对于 GET 请求，返回渲染后的页面；对于 POST 请求，则获取提交的表单数据并保存。为了在函数内加以区分，我们添加一个
if 判断处理。

### 请求对象

Flask 会在请求触发后把请求信息放到 request 对象里，你可以从 flask 包导入它：

```python
from flask import request
```

因为它在请求触发时才会包含数据，所以你只能在视图函数内部调用它。它包含请求相关的所有信息:

- 请求的路径（request.path）
- 请求的方法（request.method）
- 表单数据（request.form）
- 查询字符串（request.args）等等

我们首先通过 request.method 的值来判断请求方法。在 if 语句内，我们通过 request.form 来获取表单数据。request.form
是一个特殊的字典，用表单字段的 name 属性值可以获取用户填入的对应数据。

在用户执行某些动作后，我们通常在页面上显示一个提示消息。最简单的实现就是在视图函数里定义一个包含消息内容的变量，传入模板，然后在模板里渲染显示它。因为这个需求很常用，Flask
内置了相关的函数。其中 flash() 函数用来在视图函数里向模板传递提示消息，get_flashed_messages() 函数则用来在模板中获取提示消息。
flash() 的用法很简单，首先从 flask 包导入 flash 函数：

```python
from flask import flash
```

然后在视图函数里调用，传入要显示的消息内容：

```python
flash('Item Created.')
```

flash() 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，它会把数据签名后存储到浏览器的
Cookie 中，所以我们需要设置签名所需的密钥：

```python
import os

app.config['SECRET_KEY'] = os.urandom(24)
```

> 提示：这个密钥的值在开发时可以随便设置。基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里。

下面在模板（create.html）里使用 get_flashed_messages() 函数获取提示消息并显示:

```html
{% for message in get_flashed_messages() %}
<div class="alert">{{ message }}</div>
{% endfor %}
```

通过在 ```<input>``` 元素内添加 required 属性实现的验证（客户端验证）并不完全可靠，我们还要在服务器端追加验证：

```python
if not title or not year or len(year) != 4 or len(title) > 60:
    flash('Invalid input.')  # 显示错误提示
    return redirect(url_for('index'))
# ...
flash('Item created.')  # 显示成功创建的提示
```

> 提示：在正常系统开发时，会进行更严苛的验证，比如对数据去除首尾的空格。一般情况下，我们会使用第三方库（比如
> WTForms）来实现表单数据的验证工作。

### 重定向响应

重定向响应是一类特殊的响应，它会返回一个新的 URL，浏览器在接受到这样的响应后会向这个新 URL 再次发起一个新的请求。Flask
提供了 ```redirect()``` 函数来快捷生成这种响应，传入重定向的目标 URL 作为参数，比如 redirect('http://helloflask.com')。

根据验证情况，我们发送不同的提示消息，最后都把页面重定向到 create 页面，这里的主页 URL 均使用 url_for() 函数生成：

```python
  # 验证数据
if not title or not year or len(year) > 4 or len(title) > 60:
    flash('Invalid input1.')  # 显示错误提示
    flash('Invalid input2.')  # 显示错误提示
    return redirect(url_for('create'))
...
# 显示成功创建的提示
flash('Item created.')
return redirect(url_for('create'))
```

# 常用扩展

## WTForms

在 Flask 内部并没有提供全面的表单验证，所以当我们不借助第三方插件来处理时候代码会显得混乱，而官方推荐的一个表单验证插件就是
WTForms。WTForms主要用于对用户请求数据的进行验证。

### 安装 WTForms

使用 pip 执行 install wtforms 命令执行安装，如果需要支持email格式验证，还需要安装 email_validator

```bash
$ pip install wtforms
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting wtforms
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/18/19/c3232f35e24dccfad372e9f341c4f3a1166ae7c66e4e1351a9467c921cc1/wtforms-3.1.2-py3-none-any.whl (145 kB)
Requirement already satisfied: markupsafe in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from wtforms) (2.1.5)
Installing collected packages: wtforms
Successfully installed wtforms-3.1.2

$ pip install email_validator
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting email_validator
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/e4/60/b02cb0f5ee0be88bd4fbfdd9cc91e43ec2dfcc47fe064e7c70587ff58a94/email_validator-2.1.1-py3-none-any.whl (30 kB)
Collecting dnspython>=2.0.0 (from email_validator)
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/87/a1/8c5287991ddb8d3e4662f71356d9656d91ab3a36618c3dd11b280df0d255/dnspython-2.6.1-py3-none-any.whl (307 kB)
Collecting idna>=2.0.0 (from email_validator)
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/c2/e7/a82b05cf63a603df6e68d59ae6a68bf5064484a0718ea5033660af4b54a9/idna-3.6-py3-none-any.whl (61 kB)
Installing collected packages: idna, dnspython, email_validator
Successfully installed dnspython-2.6.1 email_validator-2.1.1 idna-3.6

```

### 定义表单

使用Wtforms 进行表单验证，需要定义表单类，继承于 wtforms.Form 声明表单字段类型和验证规则等，支持的表单字段有：

- StringField: 字符串字段，使用 input 标签
- PasswordField：密码字段，使用 input 标签其类型为 password
- BooleanField：复选框，使用 input 标签其类型为 checkbox
- EmailField：电子邮箱字段，使用 input 标签其类型为 email
- RadioField：单选字段，使用 select 标签
- SelectField：选择字段，使用 select 标签
- FileField：文件上传字段，使用 input 标签其类型为 file
- SubmitField：提交表单按钮字段
- 等等，查看[官方文档](https://wtforms.readthedocs.io/en/3.1.x/fields/)

表单字段一般属性：

- name: 此字段的HTML表单名称。这是在表单中定义的名称，加上传递给表单构造函数的前缀。
- short_name: 该字段的无前缀名称。
- id:该字段的HTML ID。如果未指定，则为您生成与字段名称相同的名称。
- label:标签可以打印成HTML标签，当作为字符串计算时返回一个HTML结构。```<label for="id">```
- default:设置表单字段的默认值
- description：字段的描述，一般用于帮助文本
- errors：包含此字段的验证错误的列表
- process_errors：输入处理过程中获得的错误。在验证时，这些错误将被添加到错误列表中
- widget：负责渲染网页上HTML表单的输入元素和提取提交的原始数据。widget是字段的一个内在属性，用于定义字段在浏览器的页面里以何种HTML元素展现。
- type：该字段的类型，以字符串形式表示。这可以在你的模板中使用，根据字段的类型做逻辑。
- flags：包含由字段本身或字段上的验证器设置的标志的对象。例如，InputRequired，未设置标志将导致 None
- meta：表单的元素据
    - csrf = False，将 csrf 设置为True将为表单启用 csrf。该值也可以通过实例化时定制来覆盖每个实例(
      例如，如果csrf只在特殊情况下需要关闭)。
    - csrf_field_name = 'csrf_token'，自动添加的 csrf 令牌字段的名称。
    - 等等，详细查看[官方文档](https://wtforms.readthedocs.io/en/3.1.x/meta/)
- filters：与传递给字段构造函数的过滤器序列相同。

```python
from wtforms import Form, StringField, validators, PasswordField, SubmitField


class LoginUserForm(Form):
    email = StringField('登陆邮箱',
                        validators=[validators.data_required(), validators.email(message="请输入注册的邮箱地址")])
    password = PasswordField('登录密码', validators=[validators.data_required(),
                                                     validators.length(min=8, max=12, message="密码最少8位，最多12位。")])
    submit = SubmitField("登录")
```

```python
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        form = LoginUserForm()
        return render_template("login.html", form=form)
    else:
        form = LoginUserForm(formdata=request.form)
        if form.validate():  # 对用户提交数据进行校验，form.data是校验完成后的数据字典
            print("用户提交的数据用过格式验证，值为：%s" % form.data)
            return "登录成功"
        else:
            print(form.errors, "错误信息")
        return render_template("login.html", form=form)
```

```html
{% extends 'base/base.html' %}
{% block content %}
<form method="post">
    {% for field,err in form.errors.items() %}
    {% for e in err %}
    <div class="alert">{{field}}:{{ e }}</div>
    {% endfor%}
    {% endfor%}
    <p>{{form.email.label}} {{form.email}}</p>
    <p>{{form.password.label}} {{form.password}} </p>
    <p>{{form.submit}} </p>

</form>
{% endblock %}
```

## Bootstrap-Flask

Bootstrap-Flask 是 Bootstrap 和 Flask 的 Jinja 宏集合。它可以帮助您 更轻松地将与 Flask 相关的数据和对象呈现为 Bootstrap
HTML标签。

### 安装 Bootstrap-Flask
使用 pip 执行 install bootstrap-flask flask-wtf 命令安装 
```bash
$ pip install bootstrap-flask
Looking in indexes: https://pypi.tuna.tsinghua.edu.cn/simple
Collecting bootstrap-flask
  Downloading https://pypi.tuna.tsinghua.edu.cn/packages/95/e4/7f3dd2dba1ef70ddbf1bf6a58ea8245c20b2d44bd81e8b37215e812f5d0e/Bootstrap_Flask-2.3.3-py2.py3-none-any.whl (3.9 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.9/3.9 MB 1.5 MB/s eta 0:00:00
Requirement already satisfied: Flask in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from bootstrap-flask) (3.0.2)
Requirement already satisfied: WTForms in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from bootstrap-flask) (3.1.2)
Requirement already satisfied: Werkzeug>=3.0.0 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from Flask->bootstrap-flask) (3.0.1)
Requirement already satisfied: Jinja2>=3.1.2 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from Flask->bootstrap-flask) (3.1.3)
Requirement already satisfied: itsdangerous>=2.1.2 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from Flask->bootstrap-flask) (2.1.2)
Requirement already satisfied: click>=8.1.3 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from Flask->bootstrap-flask) (8.1.7)
Requirement already satisfied: blinker>=1.6.2 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from Flask->bootstrap-flask) (1.7.0)
Requirement already satisfied: markupsafe in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from WTForms->bootstrap-flask) (2.1.5)
Requirement already satisfied: colorama in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from click>=8.1.3->Flask->bootstrap-flask) (0.4.6)
Installing collected packages: bootstrap-flask
Successfully installed bootstrap-flask-2.3.3

Collecting flask-wtf
  Using cached https://pypi.tuna.tsinghua.edu.cn/packages/02/2b/0f0cf68a2f052ea3dbb8b6c8c2a7e8aea5e6df7410f5e289437fefbeb461/flask_wtf-1.2.1-py3-none-any.whl (12 kB)
Requirement already satisfied: flask in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from flask-wtf) (3.0.2)
Requirement already satisfied: itsdangerous in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from flask-wtf) (2.1.2)
Requirement already satisfied: wtforms in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from flask-wtf) (3.1.2)
Requirement already satisfied: Werkzeug>=3.0.0 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from flask->flask-wtf) (3.0.1)
Requirement already satisfied: Jinja2>=3.1.2 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from flask->flask-wtf) (3.1.3)
Requirement already satisfied: click>=8.1.3 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from flask->flask-wtf) (8.1.7)
Requirement already satisfied: blinker>=1.6.2 in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from flask->flask-wtf) (1.7.0)
Requirement already satisfied: markupsafe in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from wtforms->flask-wtf) (2.1.5)
Requirement already satisfied: colorama in c:\users\develop\anaconda3\envs\flask-dev\lib\site-packages (from click>=8.1.3->flask->flask-wtf) (0.4.6)
Installing collected packages: flask-wtf
Successfully installed flask-wtf-1.2.1
```

### 初始化
