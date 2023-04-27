
"""
Flask学习资料：
    https://zhuanlan.zhihu.com/p/137655320
    https://zhuanlan.zhihu.com/p/104273184
    https://tutorial.helloflask.com/ready/
    https://blog.csdn.net/weixin_45950544/article/details/104067405

Flask基础：
    作为web框架，flask只保留了核心功能：请求响应处理和模板渲染。这两类功能分别由 Werkzeug（WSGI 工具库）完成和 Jinja（模板渲染库）完成

    除了采用session会话、cookie等缓存技术外，flask框架也提供了处理上下文的方式全局g对象和context，处理公共变量存储使用问题。

Flask蓝图(blueprint)类：
    蓝图是flask框架为解决项目框架搭建的工具，用于分业务模块来配置路由及模型
    user=Blueprint('user',__name__)  # 蓝图使用方法，参数里给定文件名，还可以给定url前缀
    @user.route('/login')   #使用user的路由配置
    def loginpage():
        return render_template("login.html")

视图函数的参数说明：参数要写在<>中，如<int: user_id>;视图函数的参数要与路由中的一致;也可以限定参数类型（int/float/path），默认是字符串

视图函数名：作为代表某个路由的端点（endpoint），同时用来生成视图函数对应的 URL。对于程序内的 URL，为了避免手写，
    Flask 提供了一个 url_for 函数来生成 URL，它接受的第一个参数就是端点值，默认为视图函数的名称。可以理解为视图函数名和对应URL的映射。

"""

from flask import request, url_for, session, Response, Blueprint, render_template, Flask, g, flash
from werkzeug.utils import redirect
from markupsafe import escape
from flask_login import login_required, LoginManager
from .models import User


app = Flask(__name__)  # 实例化并命名为app实例


def get_request_info():
    print("获取本次请求信息：")
    print(f"{request.url}")
    print(f"{request.method}")
    print(f"{request.remote_addr}")
    print(f"{request.host_url}")
    print(f"{request.form}")


@app.route("/login")  # 调用route路由方法，设置路由路径
@app.route("/register")
@app.route("/logout/<param_name>")  # 一个视图函数可绑定多个URL
@app.route("/user/<param_name>", methods=["GET", "POST"])  # 可以在 URL 里定义变量作为请求的参数, methods指定该视图函数能处理的HTTP请求类型，默认之能接受GET请求
def login(param_name):
    if request.method == "POST":
        print("获取页面提交的数据，并保存在目标位置")
        username = request.form.get("username")  # 获取页面填写的值，username表示获取<input>标签的name属性值为username的文本框的值
        # 添加表单信息验证，并根据验证结构发送不同的提示信息给页面
        if username != "":
            flash(f"{username}注册成功")  # flash用来在视图函数里向模板传递提示消息，get_flashed_messages() 函数则用来在模板中获取提示消息。
        else:
            flash(f"注册失败，填写的信息不符合要求")
        return redirect(url_for("login"))  # 注册成功后，重定向到登录页面
    elif request.method == "LOGOUT":
        print("注销登录")
    else:
        print("默认渲染页面")
        print("当前用户为：{}".format(param_name))
        print("函数名和对应URL的映射：", url_for("display_homepage", user="star"))
        print("函数名和对应URL的映射：", url_for("display_homepage", num="2"))  # num是多余的关键字参数，会被作为查询字符串附加到 URL 后面
        return render_template("UserLogin.html")  # 返回HTML页面
    # return "这是登录页面内容：%s" % "服务器返回的内容"  # 返回静态字符串或HTML代码皆可


@app.route('/loginProcess', methods=['POST', 'GET'])
def loginProcesspage():
    if request.method == 'POST':
        nm = request.form['nm']  # 获取姓名文本框的输入值
        pwd = request.form['pwd']  # 获取密码框的输入值
        if nm == 'cao' and pwd == '123':
            session["username"] = nm  # 用户会话存储，使用session方式，session默认为数组，给定key和value即可
            return redirect(url_for('homopage'))  # 重定向页面，redirect默认参数里没有传值功能，因此如这种用户注册，需要使用一下会话session缓存技术
        else:
            return 'the username or userpwd does not match!'  # 返回值默认会被浏览器作为 HTML 格式解析
    return Response("xxxxxxxxxxxxxxx")
    return {"msg": "success", "data": {"id": u_id, "username": 'yuz', "age": 18}}  # 也可直接返回数据
    return '<h3>welcome to my webpage!</h3><hr><p style="color:red">直接返回HTML代码</p>'


@app.route("/watchlist")  # 调用route路由方法，设置路由路径
@get_request_info
def display_homepage():
    print("进入站点首页")
    return render_template("HomePage.html")  # 返回HTML页面并传递数据


@app.route("/details/<username>", methods=["GET"])  # 调用route路由方法，设置路由路径
# @login_required  # 登录视图保护：禁止未登录用户访问的页面；模板内容保护：对未登录用户隐藏页面内容
def display_details():
    msg = {"a": "aaa", "b": "bbb"}  # 要返回给页面的数据
    return render_template("HomePage.html", data=msg)  # 返回HTML页面并传递数据


# 自定义错误页面，使用 app.errorhandler() 装饰器注册一个错误处理函数，当 指定错误编码类型的错误发生时，函数会被触发，返回值会作为响应主体返回给客户端
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('ErrorPage.html')  # 返回模板和状态码


# 模板上下文处理函数：统一注册多个模板内都需要使用的变量，此函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}


if __name__ == "__main__":
    app.run()  # 默认启动内置服务器，监听地址为本地的5000端口，默认返回界面为 404 页面无法找到
    # app.run(port=2020, host="127.0.0.1", debug=True, theaded=True)  # 调用run方法启动服务，自定义服务器地址和端口号，debug：代码更新是否自动重启，theaded：是否开启多线程
