from flask import request, redirect, url_for, Flask, flash, render_template
from flask_login import login_required, LoginManager, login_user, logout_user
from models import User

account = Flask(__name__)


@account.route("/login", methods=["GET", "POST"])
def login():
    """显示登录页面，处理登录请求"""
    if request.method == "POST":
        print("获取登录信息并进行验证")
        username = request.form.get("username")  # 获取页面填写的值，username表示获取<input>标签的name属性值为username的文本框的值
        password = request.form.get("username")

        if not username or not password:
            flash("登录验证失败：用户名或密码为空")
            return redirect(url_for("login"))  # 重定向到登录页面

        # 添加表单信息验证，并根据验证结构发送不同的提示信息给页面
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash("用户登录成功")  # 页面提示
            return redirect(url_for("homepage"))  # 重定向到首页(登录后的)
        flash("用户名或密码错误，请重新输入")
        return redirect(url_for("login"))  # 重定向到登录页面
    else:
        return render_template("UserLogin.html")  # 直接打开登录页面


@account.route("/logout")
@login_required
def logout():
    """注销登录"""
    logout_user()  # 登出用户
    flash(f"用户已退出登录")  # 页面提示
    return redirect(url_for("homepage"))  # 重定向到首页


@account.route("/register")
def register():
    """用户注册"""
    print("发起用户注册请求")
    flash("请填写信息完成注册")
    return render_template("UserRegistr.html")  # 打开注册页面

